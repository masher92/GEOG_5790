# -*- coding: utf-8 -*-
"""
File which....
@author Molly Asher
@Version 1.0-SNAPSHOT
@license
"""

# Change again

# pip install lxml
from lxml import etree 
import os

### Set working directory
os.chdir ("M:/Geog5990/Practical7-XML")

def readXML (XML_file):
    """
    Open an XML file and edit encoding.
    : param xml_file: The filepath to the XML to connect to.
    : return: the root file of the XML document
    """
    xml = open(XML_file).read() # Open xml file
    # Remove xml file's encoding element of prologs 
    xml = xml.replace('<?xml version="1.0" encoding="UTF-8"?>',"")
    # create a root from the xml file
    root = etree.XML(xml)
    return(root)

def validateXML_xsd (root, schema_file):
    """
    Validate an XML root file using an XSD schema file
    : param root: A root of an XML file.
    : param schema_file: An XSD schema file.
    : return: a printed statement defining whether the XML is validated.
    """
    # Open xsd schema file 
    xsd_file = open(schema_file) 
    # Parse the schema file, and turn into an XML scheme validator
    xsd = etree.XMLSchema(etree.parse(xsd_file))
    # Run the validation and print the result 
    print(xsd.validate(root))

def validateXML_dtd(root, schema_file):
    """
    Validate an XML root file using an DTD schema file
    : param root: A root of an XML file.
    : param schema_file: A DTD schema file.
    : return: a printed statement defining whether the XML is validated.
    """
    #  Open dtd schema file 
    dtd_file = open(schema_file) 
    # Parse the schema file, and turn into an XML scheme validator
    dtd = etree.DTD(dtd_file)
    # Run the validation and print the result 
    print(dtd.validate(root))
    
def writeXML (file_to_write, write_location, write_mode):
    '''
    Write an XML file to a folder.
    : param file_to_write: the XML file to write to folder.   
    : param write_location: folder location to write XML file to.
    : param write_mode: mode, a string indicating how the file is to be opened.
    : return: [Nothing]
    '''
    writer = open(write_location, write_mode) # Open for binary write
    writer.write(file_to_write)
    writer.close()

def transformXML (stylesheet, root):
    '''
    Transform an XML object into a different format using a stylesheet.
     : param stylesheet: an xsl stylesheet file .   
     : param root: the root of the XML file to be transformed.  
     : return: the XML tranformed into the new format. 
    '''
    # Read in XML stylesheet
    xslt = readXML (stylesheet)
    # Make transform object
    transform = etree.XSLT(xslt)		
    # Transform some XML root
    result_tree = transform(root)			
    transformed_text = str(result_tree)
    return (transformed_text)
    
# Create roots.
root_map1 = readXML ("map1.xml")
root_map2 = readXML ("map2.xml")
        
# Run validations using xsd and dtd methods.
validateXML_xsd(root_map2, "map2.xsd")
validateXML_dtd(root_map1, "map1.dtd")

#List elements of the XML.
print (root_map1.tag) 	
print (root_map1[1].tag)			# "polygon"
print (root_map1[0].get("id"))		# "p1"
print (root_map1[0][0].tag)		    # "points"
print (root_map1[0][0].text)		# "100,100 200,100" etc.

# Add a new polygon 
p2 = etree.Element("polygon2")				# Create polygon
p2.set("id", "p2");					        # Set attribute
p2.append(etree.Element("points"))			# Append points
p2[0].text = "100,100 100,200 200,200 200,100"	# Set points text
root_map1.append(p2)						# Append polygon
print (root_map1[1].tag)					# Check
out = etree.tostring(root_map1, pretty_print=True)
print(out)

#### Write altered xml to a file
writeXML(out, 'xml4.xml', 'wb')

### Transform the XML
transformed_text = transformXML("map3.xsl", root_map1)

# Write to file
writeXML (transformed_text,'map3.html', 'w' )
