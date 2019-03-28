## Project 2 - Scripts

This project builds on the contents of Practical 1 - Model Builder.     
It continues to work on tools to model the impact of a bomb exploding on the buildings in its vicinity using Arcmap.    
In Practical 1 a ModelBuilder model was created which accomplished this in ArcMap. The ModelBuilder Model was also converted into a script which could run the same process inside ArcMap.  

The file "RunModelFromScript":  
Is an external (and standalone script) which runs the BombExplosion model created in ModelBuilder and stored in the Practical1_Models.tbx. 
It takes as inputs: 
* A shapefile containing the location of an explosion.
* A shapefile containing the outlines and locations of the surrounding buildings.
* A distance at which the impact of the explosion is felt.
It returns as outputs:
* A shapefile containing the outlines of the buildings impacted by the explosion.

The file :

			






* A script to convert a "layer" file into a shapefile.


To run file from cmd:
C:\Python27\ArcGIS10.6\python.exe external.py

