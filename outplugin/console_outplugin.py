from outplugin import OutPlugin


class ConsoleOutPlugin(OutPlugin):
    def __init__(self):
        OutPlugin.__init__(self)
    
    def push(self,refineddata):
        if refineddata:
            for fvalue in refineddata:
                print fvalue.__dict__.__str__() + "\n"