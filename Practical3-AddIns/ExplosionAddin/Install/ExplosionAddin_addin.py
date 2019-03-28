import arcpy
import pythonaddins

class ExplosionButtonClass(object):
    """Implementation for ExplosionAddin_addin.explosionbutton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
          object = pythonaddins.GPToolDialog("E:/MSc/Advanced-Programming/GitHub/GEOG_5790/Practical2-Scripts/Explosion Toolbox (v2).tbx", "Explosion") 
       
