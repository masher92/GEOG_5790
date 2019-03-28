## Project 3 - AddIns

This project builds on the contents of Practical 1 and Practical 2: continuing to work on tools to model the impact of a bomb exploding on the buildings in its vicinity using Arcmap.    
It creates an AddIn\* button which can be used to open the Geoprocessing toolbox that was created in Practical 2 and to run the Model within it.  
The Add-In generates a dialogue box prompting the user to supply the parameters required by the model, namely:  
* A shapefile containing the location of an explosion.  
* A shapefile containing the outlines and locations of the surrounding buildings.  
* A distance at which the impact of the explosion is felt.  

In order to use the Add-In, the .esriaddin file must be rebuilt and the install addin wizard run.   
The "ExplosionAddin_addin.py" file in the Install folder, and the text inside 'onclick', can be used to change the functionality associated with the Add-In.    

\* An Add-in is a customised plug in to ArcGIS desktop which allow custom tasks to be completed by supply supplementary functions.  
More information about building Add-Ins can be found here: http://desktop.arcgis.com/en/arcmap/latest/analyze/python-addins/creating-an-add-in-project.htm

Improvements:  
* Change the message outputting functionality so it gives progress report.