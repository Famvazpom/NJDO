import PyPDF2
import re

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