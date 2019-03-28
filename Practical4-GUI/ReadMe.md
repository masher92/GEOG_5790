## Project 4 - GUI

This project builds a toolbar in ArcGIS for analysing the risk of burglary. 

Research suggests that in the 4 weeks following a house getting burgled there is an increased risk of burglary for the houses in the burgled house's immediate vicinity.
This model uses this theory to analyse the probability of houses in an area getting burgled.  

The project includes:
* The Practical4Models.tbx which contains the "TraffordModel" constructed in ArcMap's ModelMaker which defines the process for modelling the risk of burglary in an area.
* The "TraffordModelScript.py" which runs the "TraffordModel" from Practical4Models.tbx as a tool in ArcGIS and processes the results further in order to sort the outputs
according to risk and to display it colour coded by this level of risk. 
* A Practical4.mxd file which is required in the creation of this colour-coded display.
* An AddIn folder which generates an Add-In toolbar for use in ArcMap with a button that runs the "TraffordModelScript.py" from within "Practical4Models.tbx"



