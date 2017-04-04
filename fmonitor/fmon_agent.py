import sys
import os
sys.path.extend(["../../fmone"]) # For Docker we set the PYTHONPATH two levels above to import the whole project.
from inplugin import inplugin_factory
from outplugin import outplugin_factory
from midplugin import midplugin_factory
import time


class FMonAgent():
    def __init__(self,period,inplugin,midplugin,outplugin,**args):
        try:
            self.inplugin = inplugin_factory.getinplugin(plugin_type=inplugin)
            self.midplugin = midplugin_factory.getmidplugin(plugin_type=midplugin,)
            self.outplugin = outplugin_factory.getoutplugin(plugin_type=outplugin,**args)
            self.period = period
        except ValueError as err:
            print(err.args)

    def run(self):
        while True:
            time1 = time.time()
            self.inplugin.collect()
            listofvalues = self.inplugin.pop()
            refinedvalues = self.midplugin.refine(listofvalues)
            self.outplugin.push(refineddata=refinedvalues)
            time2 = time.time()
            timediff = time2-time1
            time.sleep(self.period - timediff)


if __name__ == '__main__':
    home = os.environ['HOME']
    fmonagent = FMonAgent(5,"cpu","inout","file",outfilepath= home + "/fmone.txt")
    fmonagent.run()