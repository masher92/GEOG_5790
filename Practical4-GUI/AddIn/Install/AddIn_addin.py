import arcpy
import pythonaddins

class RiskButton(object):
    """Implementation for AddIn_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # Print message to confirm initialisation
        pythonaddins.MessageBox("I am working", "Working?")
        # Run toolbox
	pythonaddins.GPToolDialog("E:/Msc/Advanced-Programming/GitHub/GEOG_5790/Practical4-GUI/Practical4Models.tbx", "TraffordModelScript")
        pass
