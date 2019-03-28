## Project 3 - AddIns

This project builds on the contents of Practical 1 and Practical 2.    
It continues to work on tools to model the impact of a bomb exploding on the buildings in its vicinity using Arcmap.    
It creates an AddIn/* button which can be used to open the Geoprocessing toolbox that was created in Practical 2 and to run the Model within it.  
This creates a dialogue box prompting the user to supply the parameters required by the model:  
* A shapefile containing the location of an explosion.  
* A shapefile containing the outlines and locations of the surrounding buildings.  
* A distance at which the impact of the explosion is felt.  

In order to use the Add-In, the .esriaddin file must be rebuilt and the install addin wizard run.   
In order to change the content of the Add-In the "ExplosionAddin_addin.py" file in the Install folder must be used.   
The text inside 'onclick' can be altered to change the functionality associated with the Add-In.  

/* An Add-in is a customised plug in to ArcGIS desktop which allow custom tasks to be completed by supply supplementary functions.  

