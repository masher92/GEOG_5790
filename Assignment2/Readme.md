## Sampling location generator 
The purpose of this program is to provide a user with a set of locations in which to conduct manual sampling
of peat depth in order to optomise performance of a geostatistical model of peat depth over an area of interest.

If the user has an existing dataset of locations where they have sampled peat depth previously, the program can
identify locations where additional sampling would improve the utility of the dataset.  

The program is designed to ensure the sample:
* A.) Contains the number of samples desired by the user.
* B.) Has the same proportional representation of slope and elevation categories as the wider AOI.
* C.) Ensures that each sample point is within a specified distance range of at least one other point.

## Motivation 
Peatlands contain a large proportion of the global soil organic carbon pool and provide vital key ecosystem services.
Knowledge of the depth, and subsequently volume, of peat stored in blanket peatlands is therefore of value.
Peat depth varies over small spatial scales and capturing this varibality through both fine-scale manual sampling 
and geophysical techniques such as remote sensing or ground penetrating radar is expensive.
An alternative approach involves modelling peat depth using variables known to influence peat depth, 
e.g. slope and elevation, which are readily available in public datasets.
These models can be fitted using samples of peat depth measured manually. 


## Installation/ A quickstart tutorial on how to ues it requirements, installation, configureaiton, how to use it.
 

## License

## Example usage?

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
