## Project 3 - AddIns

This project builds on the contents of Practical 1 and Practical 2 and is based on creating tools to model the impact of a bomb exploding on the buildings in its vicinity using Arcmap.    

It creates an AddIn\* button which can be used to open the Geoprocessing toolbox that was created in Practical 2 and to run the Model within it.  

The Add-In generates a dialogue box prompting the user to supply the parameters required by the model, namely:  
* A shapefile containing the location of an explosion.  
* A shapefile containing the outlines and locations of the surrounding buildings.  
* A distance at which the impact of the explosion is felt.    

It also requires the user where to specify the output, namely:
* A shapefile containing the outlines of the buildings destroyed by the bomb.

<ins> In order to install the AddIn:</ins> 
* Open the AddIn folder and run the "makeaddin.py" file and the .esriaddin file to install the addin.
* Open ArcGIS and go to "Customize" on top toolbar and select "AddIn Manager" to check the addin is installed.
* If the add-in appears then select "customise", click the toolbars tab and scrool down to the "Explosion" toolbar and ensure it is selected.
* Addin should now appear somewhere floating on docked to one of the top toolbars.

<ins>  In order to edit the Addin and change the functionality associated with the Add-In: </ins> 
* Open the "ExplosionAddin_addin.py" file in the Install folder.
* Edit the text inside the class 'onclick

\* <i> An Add-in is a customised plug in to ArcGIS desktop which allow custom tasks to be completed by supply supplementary functions. More information about building Add-Ins can be found here: http://desktop.arcgis.com/en/arcmap/latest/analyze/python-addins/creating-an-add-in-project.htm </i>

Improvements:  
* Change the message outputting functionality so it gives progress report.
