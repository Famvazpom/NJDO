import PyPDF2
import re
import csv

class object():

    def search(self,file,codes):
        results = {}
        for i in codes:
            results[i] = []

        object = PyPDF2.PdfFileReader(file)
        NumPages = object.getNumPages()

        for i in range(0,NumPages):
            PageObj = object.getPage(i)
            Text = PageObj.extractText()
            for String in codes:
                ResSearch = re.search(String, Text)
                if ResSearch:
                    results[String].append(str(i))
        return results
    
    def loadCodeFile(self):
        try:
            with open('codes.cfg', 'r') as cfgfile:
                codes = []
                reader = csv.reader(cfgfile,delimiter=',')
                for row in reader:
                    for value in row:
                        codes.append(value)
                return codes
        except IOError:
            return False

    def saveCodes(self,codes):
        try:
            with open("codes.cfg", 'w') as cfgfile:
                wr = csv.writer(cfgfile, quoting=csv.QUOTE_ALL)
                wr.writerow(codes)
            return True
        except IOError:
            return False