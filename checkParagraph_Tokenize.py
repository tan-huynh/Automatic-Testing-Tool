import nltk
import re
import os
import glob
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path

# Program to measure similarity between  
# two sentences using cosine similarity. 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# (?s)((?:[^\n][\n]?)+)

txtStart = []
txtEnd = []

m = 0
n = 0

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
infile = askopenfilename(
    initialdir="/home/huynh/work/elisa2/test/ui/squish/EPC",
    title = "Open A File",
    filetypes=(("feature files", "*.feature"), ("All Files", "*.*"))	
) # show an "Open" dialog box and return the path to the selected file

text = Path(infile).read_text()       

for match in re.finditer(r"(^\s{0,}Scenario(?:[^\n][\n]?)+)", text, re.VERBOSE | re.MULTILINE):
   txtStart.append(match.start())
   txtEnd.append(match.end())
   #print(match.start(), match.end())
   #print(text[match.start():match.end()])
print(txtStart)
print(txtEnd)

def different2Scenarios(a: str, b: str):
    X = a.lower()
    Y = b.lower()

    # tokenization 
    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 
      
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
      
    # remove stop words from string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
      
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
      
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    return cosine

for m in range(len(txtStart)):
    n = m + 1
    while(n<len(txtStart)): 
        C1=text[txtStart[m]:txtEnd[m]]
        C2=text[txtStart[n]:txtEnd[n]]
        print(f"Similarity ratio of {txtStart[m], txtStart[n]}:", different2Scenarios(C1, C2))
        n = n + 1
    m = m + 1

