#edit to process non TEI and TEI file
import xml.etree.ElementTree as ET
def extractTextTEI(fileName, isTEI=0):
	f = open(fileName, "r")
	strFile = f.read()
	strFile = strFile.replace(" &", " _ ")
	strFile = strFile.replace(" <", " _ ")
	if (isTEI):
		root = ET.fromstring(strFile)
		out = ""
		for content in root.iter('sent'):
			out = out + " " + content.text
	else:
		out = strFile
	f.closed
	return out

# https://docs.python.org/2/tutorial/inputoutput.html
# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.iter

# https://docs.python.org/2/tutorial/inputoutput.html
# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.iter