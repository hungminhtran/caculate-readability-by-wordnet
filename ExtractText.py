import xml.etree.ElementTree as ET
def extractTextTEI(fileName, isTEI=0):
	f = open(fileName, "r")
	if (isTEI):
		out = ""
		root = ET.fromstring(f.read())
		for content in root.iter('sent'):
			out = out + " " + content.text
	else:
		out = f.read()
	f.closed
	return out

# https://docs.python.org/2/tutorial/inputoutput.html
# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.iter
