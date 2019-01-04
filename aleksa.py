import sys
import uuid

"""
Object <> Task List <> 
Shot <> Roto, Paint, Comp | 

Object  <%>  Condition
Roto    <%>  ItemList   <%>  Range()
                             ScreenLocation()
                             AnnotColor()
                             Annotation()
                             
                             
Shot    <%>  TaskList
             Description()
             Range()
             Globals()

"""

class Constraint(object):
    def __init__(self, parent=None):
        """
        Constraint
        """
        self.id = str(uuid.uuid4())
        self._required = False
        self.parent = parent
        if parent:
            self.parent.add_constraint(self)

    def __repr__(self):
        return "%s:: %s" %( self.__class__.__name__, self._rapr() )

    def _rapr(self, txt):
        return ""

    def _satisfied(self):
        ret = False
        if self.satisfied() == True:
            ret = True
        else:
            if self._required == True:
                pass
            else:
                ret = True
        return ret

    def satisfied(self):
        return True

class Choice(Constraint):
    def __init__(self, choices, **kwargs):
        self._choices = choices

class Text(Constraint):
    def __init__(self, txt, **kwargs):
        self.value = txt

class ObjectList(Constraint):
    """
    Constraint: must give me objects
    """
    def __init__(self, objects=None, limit_type=None, **kwargs):
        super(ObjectList, self).__init__(**kwargs)
        self._type_limit = []
        self._objs = {}
        if objects:
            if type(objects) == type([]):
                self.add(*objects)
        if limit_type:
            if type(limit_type) == type([]):
                self.limit_to(*limit_type)
            elif type(limit_type) == type(""):
                self.limit_to(limit_type)

    def _rapr(self):
        tp = "Everything"
        if self._type_limit != []:
            tp = ", ".join(sorted(self._type_limit))
        return "(%s):: %d objects." %(tp, len( self._objs.keys() ))

    def satisfied(self):
        ret = False
        if len(self._objs.keys())>0 and all([(v.type in self._type_limit) for i,v in self._objs.iteritems()]):
            return True

    def limit_to(self, *obj):
        self._type_limit = []
        for o in obj:
            self._type_limit.append( o.type )

    def add(self, *obj):
        """
        Adds an item to the list.
        :param obj:
        :return:
        """
        rej = []
        com = []
        for o in obj:
            if self._type_limit != []:
                if o.type in self._type_limit:
                    self._objs[o.id] = o
                    com.append(o)
                else:
                    rej.append(o)
            else:
                self._objs[o.id] = o
                com.append(0)
        print "Added %d items to list." %len(com)
        if len(rej)>0:
            print "Rejected %d restricted items of types: (%s)" %(len(rej), ", ".join([i.type for i in rej]))

class ScreenLocation(Constraint):
    def __init__(self, z=None, xy=None, **kwargs):
        super(ScreenLocation, self).__init__(**kwargs)
        self._z_possibilities = sorted(self._mk_poslist("BG", 5) + self._mk_poslist("FG", 5) + self._mk_poslist("MG", 5))
        self._xy_possibilities = ["USL", "UC", "USR",
                                  "CSL", "CC", "CSR",
                                  "LSL", "LC", "LSR"]

        self._xy_positional_keys = { 0 : { "U" : "Upper", "C" : "Center", "L" : "Lower"},
                                     1:  { "S" : "Screen", "C" : "Center" },
                                     2:  { "L" : "Left", "R" : "Right"}
                                     }

        self._z  = z
        self._xy = xy


    def _mk_poslist(self, pos, len=4):
        return sorted(["%s%d" %(pos, f+2) for f in list(range(len-1))]+[pos])

    def _pos_code_to_text(self, code):
        ostr = ""
        for c, i in enumerate(code):
            ostr+= (self._xy_positional_keys[c][i] + " ")
        return ostr

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, pos):
        if pos in self._z_possibilities:
            self._z = pos
        else:
            raise Exception("Not a valid position. Please use one of the following: [%s]" %(", ".join(self._z_possibilities)))

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, pos):
        if pos in self._xy_possibilities:
            self._xy = pos
        else:
            raise Exception("Not a valid position. Please use one of the following: [%s]" % (", ".join(self._xy_possibilities)))

    def satisfied(self):
        ret = False
        if self._z and self._xy:
            ret = True
        return ret



class Range(Constraint):
    def __init__(self, start=None, end=None, **kwargs):
        super(Range, self).__init__(**kwargs)
        self._start = start
        self._end = end

    def __repr__(self):
        if self._start and self._end:
            return "%s (%d-%d)" %(self.__class__.__name__, self._start, self._end)
        else:
            return "%s (None)" % (self.__class__.__name__)

    def satisfied(self):
        ret = False
        if self._start and self._end:
            ret = True
        return ret

    @property
    def range(self):
        return (self._start, self._end)

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end



class Object(object):
    def __init__(self, type=None, text=None, parent=None):
        self.id = str(uuid.uuid4())
        self._type = type
        self._text = text
        self._constraints = {}
        self._parent = None


    def add_constraint(self, constraint):
        self._constraints[constraint.id] = constraint

    def __repr__(self):
        return "%s (%s): '%s'" %(self.__class__.__name__, self.type, self.text)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, tp):
        self._type = tp

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, tx):
        self._text = tx

    def _validation_map(self):
        val = dict((v.id, v.satisfied()) for k, v in self._constraints.iteritems())
        return val

    def validate(self):
        m = self._validation_map()
        invalid = [i for i,v in m.iteritems() if v is False]
        if len(invalid)>0:
            return  (False, invalid)
        else:
            return  (True, self._constraints.keys())

    def tree(self, indent=0):
        ind = indent+1
        print "%s [%s] (%s)" % ("\t" * (ind - 1), self.__class__.__name__, self._type)
        for i, v in self._constraints.iteritems():
            print "%s[%s] %s" %("\t"*ind, v.__class__.__name__, v.id)
            if isinstance( v, ObjectList):
                listitems = [p for o,p in getattr(v, "_objs").iteritems()]
                for l in listitems:
                    l.tree(ind+1)





shot = Object("Shot")
shot_range = Range(parent=shot)
task_list = ObjectList(parent=shot)

roto_task = Object("RotoTask")
trk_task = Object("TrackingTask")
task_list.add( roto_task, trk_task )

roto_obj_list = ObjectList(parent=roto_task)



for i in ["person", "place", "thing"]:

    rotoobj = Object("RotoObject", text=i)
    constr = Range(parent=rotoobj)
    roto_obj_list.add( rotoobj )

