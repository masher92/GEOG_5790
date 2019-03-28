## Project 2 - Scripts

This project builds on the contents of Practical 1 - Model Builder.   
It continues to work on tools to model the impact of a bomb exploding on the buildings in its vicinity using Arcmap.
In Practical 1 a model was developed to do this which could be run from inside of ArcMap.  
This project converts this script so that it can be run externally to ArcMap.    

These tools include:
* A script to convert a "layer" file into a shapefile.
			
It takes as inputs: 
* A shapefile containing the location of an explosion.
* A shapefile containing the outlines and locations of the surrounding buildings.
* A distance at which the impact of the explosion is felt.
It returns as outputs:
* A shapefile containing the outlines of the buildings impacted by the explosion.

These tools include:
* An ArcMap toolbox which contains a model built with Arcmap's ModelBuilder functionality, and the same model in the format of a python script.
* A copy of the python script found in the toolbox.

Script which:
* Runs the model from the toolbox