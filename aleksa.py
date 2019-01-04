import sys
import uuid

"""
Object <> Task List <> 
Shot <> Roto, Paint, Comp | 

"""
class Constraint(object):
    def __init__(self):
        """
        Constraint
        """
        self._required = True


class ObjectList():
    def __init__(self, objects=None):
        self._type_limit = []
        self._ls = []

    def __repr__(self):
        pre = "%s of any type. Contains:" %self.__class__.__name__
        if self._type_limit != []:
            pre = "%s (%s)" %(self.__class__.__name__, ", ".join( self._type_limit )) + ". Contains:"
        return pre + "\n" +"_"*(len(pre)) +"\n" + "\n\t".join([i.__repr__() for i in self._ls])


    def limit_type(self, *obj):
        self._type_limit = []
        for o in obj:
            self._type_limit.append( o.type )


    def add(self, *obj):
        rej = []
        com = []
        for o in obj:
            if self._type_limit != []:
                if o.type in self._type_limit:
                    self._ls.append(o)
                    com.append(0)
                else:
                    rej.append(o)
            else:
                self._ls.append(o)
                com.append(0)
        print "Added %d items to list." %len(com)
        if len(rej)>0:
            print "Rejected %d restricted items of types: (%s)" %(len(rej), ", ".join([i.type for i in rej]))


class Object(object):
    def __init__(self, type=None, text=None):
        self.id = str(uuid.uuid4())
        self._type = type
        self._text = text
        self._constraints = {}

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
