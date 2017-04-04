from midplugin import MidPlugin


class InOutMidPlugin(MidPlugin):
    def __init__(self):
        MidPlugin.__init__(self)

    def refine(self,listoffvalues):
        return listoffvalues