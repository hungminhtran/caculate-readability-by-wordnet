import importlib
extractText = importlib.import_module("ExtractText")
mod1 = importlib.import_module("module-1")
for f in mod1.listAllFile('data/English Textbook 4 Readability Level', 1):
    print f
    extractText.extractTextTEI(f, 1)
    print ''