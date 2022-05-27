"""
    BLEU, or the Bilingual Evaluation Understudy, is a score for comparing a candidate translation of text to one or more reference translations.
    A perfect match results in a score of 1.0, whereas a perfect mismatch results in a score of 0.0.
    Although developed for translation, it can be used to evaluate text generated for a suite of natural language processing tasks.
"""
import nltk
from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction
import re
import os
import glob
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path

smoothie = SmoothingFunction().method4

# (?s)((?:[^\n][\n]?)+)

txtStart = []
txtEnd = []

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
C1=text[txtStart[0]:txtEnd[0]]
C2=text[txtStart[1]:txtEnd[1]]

print(f'BLEUscore ratio of {txtStart[0], txtStart[1]}',bleu([C1], C2, smoothing_function=smoothie))

