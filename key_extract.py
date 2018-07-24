import textract
import pandas as pd
import numpy as np
import re #To work with regular expressions.
import PyPDF2 #Python library to read, manipulate and extract PDF files.

#Initialize file pointer and a PdfFileReader object.
filename ='JavaBasics-notes.pdf' 
pdfFileObj = open(filename, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #It initializes a PdfFileReader object.
num_pages = pdfReader.numPages #method numPages return total number of pages in a pdf document.

#Gather all the text in document in text form.
count = 0
text = ""
while count < num_pages:
    pageObj = pdfReader.getPage(count) #Retrieves a page by number from this PDF file, and returns a pageObject.
    count = count + 1
    text = text + pageObj.extractText() #It extracts the text and returns a unicode string object.
    
#PyPDF2 can not read scanned pdf files/images. And the document provided do contain some images ,
#and might contain keywords. 

if text != "":
    text = text
else:
    text = textract.process('http://bit.ly/epo_keyword_extraction_document', method='tesseract', language ='eng')
#Now text file contain text data from pdf file.


text = text.encode('ascii', 'ignore').lower() #it encodes a unicode string to ascii and ignores errors,
#and then lowercase all words.

text = str(text) #re can't work on byte object, thus convert byte-->string. 
keywords = re.findall(r'[a-zA-Z]\w+',text)
#len(keywords)  

#len(set(keywords)) #Remove repetitions of words, and returns unique set of keywords.

df = pd.DataFrame(list(set(keywords)), columns = ['keywords'])

def key_weight(word,text,total_docs=1):
    list_of_words = re.findall(word,text) #findall return a list containing all the appearances of 'word'.
    number_of_times_word_appeared =len(list_of_words)
    tf = number_of_times_word_appeared/float(len(text)) #this returns term frequency
    idf = np.log((total_docs)/float(number_of_times_word_appeared))
    tf_idf = tf*idf
    return number_of_times_word_appeared,tf,idf ,tf_idf



df['number_of_times_word_appeared'] = df['keywords'].apply(lambda x: key_weight(x,text)[0])
df['tf'] = df['keywords'].apply(lambda x: key_weight(x,text)[1])
df['idf'] = df['keywords'].apply(lambda x: key_weight(x,text)[2])
df['tf_idf'] = df['keywords'].apply(lambda x: key_weight(x,text)[3])

df = df.sort_values('tf_idf', ascending=False)


#Store dataframe in excel sheet.
df.to_excel('keywords.xlsx', sheet_name='keywords_weight') #pip3 install openpyxl


'''
To read excel files
pip3 install xlrd
df = pd.read_excel('keywords.xlsx')'''


#Store dataframe in csv sheet
df.to_csv('keywords.csv')