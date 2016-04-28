import xml.etree.ElementTree as ET
def extractTextTEI(fileName):
	f = open(fileName, "r")
	root = ET.fromstring(f.read())
	out = ""
	for content in root.iter('sent'):
		out = out + " " + content.text
	f.closed
	return out

# https://docs.python.org/2/tutorial/inputoutput.html
# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.iter
