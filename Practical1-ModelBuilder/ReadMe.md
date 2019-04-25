## Project 1 - Model Builder

This project contains tools to model the impact of a bomb exploding on the buildings in its vicinity using Arcmap.  
The data it is based on can be found in Data/Practical1-4-Data.zip.  

These tools include:  
* An ArcMap toolbox which contains a model built with Arcmap's ModelBuilder functionality, and the same model in the format of a python script.
* A copy of the python script found in the toolbox (NB: this script is only executable from within the toolbox, it does not function as a stand alone script)
	
The model takes as inputs:  	
* A shapefile containing the location of an explosion.
* A shapefile containing the outlines and locations of the surrounding buildings.
* A distance at which the impact of the explosion is felt.

It returns as outputs:  
* A shapefile containing the outlines of the buildings impacted by the explosion.


