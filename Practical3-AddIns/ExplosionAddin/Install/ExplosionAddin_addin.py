import arcpy
import pythonaddins

class ExplosionButtonClass(object):
    """Implementation for ExplosionAddin_addin.explosionbutton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.MessageBox("Hello Molly", "Hello")
        pass
