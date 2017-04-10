from outplugin import OutPlugin


class ConsoleOutPlugin(OutPlugin):
    def __init__(self):
        OutPlugin.__init__()
    
    def push(self,refineddata):
        for fvalue in refineddata:
            print fvalue.__dict__.__str__() + "\n"