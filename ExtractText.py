#edit to process non TEI and TEI file
import xml.etree.ElementTree as ET

def extractTextTEI(fileName, isTEI=0):
    f = open(fileName, encoding='utf-8', mode='r')
    try:
        strFile = f.read()
    except:
        print("*"*10, "Error when read file with uft-8: ", fileName)
        return ["\n"]
    strFile = strFile.replace(" &", " _ ")
    strFile = strFile.replace(" <", " _ ")
    if (isTEI != 0):
        root = ET.fromstring(strFile)
        out = ""
        for content in root.iter('sent'):
            out = out + " " + content.text
    else:
        out = strFile
    f.close()
    return out

# https://docs.python.org/2/tutorial/inputoutput.html
# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.iter

# https://docs.python.org/2/tutorial/inputoutput.html
# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.iter
