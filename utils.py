import os
import sys
import json     
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

COLORS = {  "red"       : (165, 66, 61),
            "orange"    : (194, 115, 59),
            "yellow"    : (226, 184, 67),
            "olive"     : (192, 201, 81),
            "green"     : (87, 178, 98),
            "teal"      : (75, 206, 192),
            "blue"      : (78, 131, 168),
            "violet"    : (99, 72, 143),
            "purple"    : (136, 75, 147),
            "pink"      : (161, 65, 112)
}

def shrink_wrap(layout, margin=2, spacing=2):
    """

    """
    layout.setContentsMargins(margin,margin,margin,margin)
    layout.setSpacing(spacing)


def icon(name):
    ics = os.listdir( os.path.join( ROOT_DIR, "icons" )   )
    request = "%s.png" %name
    if request in ics:
        return os.path.join( ROOT_DIR, "icons", request )

class EmojiUtils(object):
    def __init__(self):
        super(EmojiUtils, self).__init__()

        self.base = "/Users/donaldstrubler/PycharmProjects/nukemoji"
        self.eac_json = "%s/eac.json" % self.base
        self.map = {}
        self.load_eac_json()

    def load_eac_json(self):
        with open(self.eac_json) as f:
            data = json.load(f)
            emoji_exists = [p.replace('.png', '') for p in os.listdir("%s/lib_128" % self.base)]
            self.map = dict((str(v['alpha_code']), str(v['output'])) for k, v in data.items() if
                            str(v['output']) in emoji_exists)

    def get_path_from_keyword(self, word):
        return "%s/lib_128/%s.png" %(self.base, self.map[":%s:" %word])

