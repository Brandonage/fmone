from outplugin import OutPlugin


class FileOutPlugin(OutPlugin):
    def __init__(self,filepath):
        OutPlugin.__init__(self)
        self.filepath = filepath

    def push(self,refineddata):
        with open(self.filepath,"a") as file:
            line = self.build_line(refineddata)
            file.write(line)

    def build_line(self,refineddata):
        line = ""
        for value in refineddata:
            line += value.__dict__.__str__() + "\n"
        return line
