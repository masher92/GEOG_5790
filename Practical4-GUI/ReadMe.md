## Project 4 - GUI

This project builds a toolbar in ArcGIS which runs a model analysing the risk of burglary for houses in an area, using:
* A shapefile of the location of previous burglaries.
* A shapefile of the location of houses in an area.  

The model is based on research which suggests that in the 4 weeks following a house getting burgled there is an increased risk of burglary 
for the houses in the burgled house's immediate vicinity.  

The project includes:
* The Practical4Models.tbx which contains the "TraffordModel" constructed in ArcMap's ModelMaker which defines the process for modelling the risk of burglary in an area.
* The "TraffordModelScript.py" which runs the "TraffordModel" from Practical4Models.tbx as a tool in ArcGIS and processes the results further in order to sort the outputs
according to risk and to display it colour coded by this level of risk. 
* A Practical4.mxd file which is required in the creation of this colour-coded display.
* An AddIn folder which generates an Add-In toolbar for use in ArcMap with a button that runs the "TraffordModelScript.py" from within "Practical4Models.tbx"

In order to install the toolbar:
* Open the AddIn folder and run the "makeaddin.py" file and the .esriaddin file to install the addin.
* Open ArcGIS and go to "Customize" on top toolbar and select "AddIn Manager" to check the addin is installed.
* If the add-in appears then select "customise", click the toolbars tab and scrool down to the "Burglary tools" toolbar and ensure it is selected.
* Addin should now appear somewhere floating on docked to one of the top toolbars.



