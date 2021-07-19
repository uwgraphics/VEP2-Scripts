# written by gleicher for internal use. see the LICENSE.txt
#
# simple attempt to convert the EEBO bibliography XML to a MetaDataBuilder compatible CSV file
# I am not an XML expert, so this may be simple

import xml.etree.ElementTree as ET
import csv
from collections import Counter

eebo_file = "Data/tls-eebo-2021-plus.xml"
fout = "Outputs/tls-eebo-2021-plus.csv"

# which columns to include
noteTypes = ["keywords","sourceLibrary","langNote","transcriptType"]
dataFields = ["title","author","pubDate","publisher","pubPlace"]

cols = ["id", "proquest", "isTcp", "tcp", "eeboIS", "type", "pages", "lang"] + noteTypes

# this is in case we need to build string names
NS = "{http://www.w3.org/XML/1998/namespace}"

# this "just does it"
tree = ET.parse(eebo_file)
root = tree.getroot()

# get an attribute if it exists, otherwise return none
# possible split at a colon - in which case we return both sides of the colon
def getAttrib(elem, attr, prop=False):
    if attr in elem.attrib:
        if prop:
            spl = elem.attrib[attr].split(":")
            if len(spl) == 2:
                return spl
            else:
                print("attribute {} has multiple splits? : ".format(attr),elem.attrib[attr])
                return elem.attrib[attr].split(":",1)
        else:
            return elem.attrib[attr]
    else:
        if prop:
            return None,None
        else:
            return None

# keep track of various types of things
noteTypes = Counter()
marcTypes = Counter()
tcpTypes = Counter()

# given an element (that is a document) - turn it into a python structure with
# the info we want
def extract(elem):
    data = {}
    unnused,data["proquest"] = getAttrib(elem,"ref",True)
    data["isTcp"],data["tcp"] = getAttrib(elem,"n",True)
    data["MARC"],data["id"] = getAttrib(elem,NS+"id",True)
    unnused,data["eeboIS"] = getAttrib(elem,"facs",True)
    data["type"] = getAttrib(elem,"type")
    data["lang"] = getAttrib(elem,NS+"lang")

    ## go through the tags and extract some of them...
    for c in elem:
        if c.tag in dataFields:
            data[c.tag] = c.text
        elif c.tag == "measure":
            if c.attrib["type"] == "pp":
                data["pages"] = c.text
            else:
                print("Unknown measure type:",c.attrib["type"])
        elif c.tag == "note":
            noteTypes[c.attrib["type"]] += 1
            if c.attrib["type"] in noteTypes:
                data[c.attrib["type"]] = c.text
    return data

# go through the books...

with open(fout,"w",newline="") as fo:
    wr = csv.writer(fo)
    # header row
    wr.writerow(cols)
    # data rows
    for i,doc in enumerate(root):
        try:
            data = extract(doc)

            ## if there were multiple splits for the TCP, pick the last one...
            ## we do this here so we can (potentially) handle this more gracefully
            ## (like making an extra record)
            if data["tcp"] and ":" in data["tcp"]:
                last = data["tcp"].split(" ")[-1]
                ni, nt = last.split(":")
                print("(item {}) Split TCP to [{},{}] - was [{},{}]".format(i,ni,nt,data["isTcp"],data["tcp"]))
                data["isTcp"] = ni
                data["tcp"] = nt

            tcpTypes[data["isTcp"]] += 1
            marcTypes[data["MARC"]] += 1

            # now write it out...
            wr.writerow([data[c] if c in data else "" for c in cols])
        except Exception as err:
            print("Error on item ",i)
            raise err

print("MARC types", marcTypes)
print("TCP types", tcpTypes)
print("note types", noteTypes)
