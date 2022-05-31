import csv
import re
import os
from pathlib import Path
import time

# Find all files in a directory with extension .feature
dir_path = os.path.dirname(os.path.realpath(__file__))
#text_files = [f for f in os.listdir(dir_path) if f.endswith('.feature')]
#Traverse all sub-directories.
text_files = []
for root,d_names,f_names in os.walk(dir_path):
    for f in f_names:
        if f.endswith('.feature'):
            text_files.append(os.path.join(root, f))

print(text_files)

k = 0
with open("findingList.csv", mode='w', encoding="utf-8") as file:
    writer = csv.writer(file)
    # Finding Phase
    while k <= len(text_files)-1:
        txt = Path(text_files[k]).read_text()
        matches = re.findall(r'Feature\:\s+[\s\S]*?(?=\n)', txt)
        #print(matches) # number of matching scenario in one feature
        i = 0
        while i <= len(matches)-1:
            for w in range(1):
                writer.writerow([matches[i], ])
                i = i + 1
        k = k + 1

# Waiting time for all data being written in findingList.csv
time.sleep(10) # Sleep for 10 seconds

def replace_words_using_dict(matchobj): # type: ignore[no-untyped-def]
    key = matchobj.group(0)
    return mydict.get(key, key)

value = input("Did you edit and save the findingList.csv with new feature names (y/Y/n/N): ")
if value in ('y', 'Y'):
    # Replacing phase
    with open('findingList.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        mydict = {(rows[0]): (rows[1]) for rows in reader}
        print(mydict)

    # Replace that text by another one
    words_to_replace = re.compile(r"\bFeature\:\s+[\s\S]*?(?=\n)\b",re.MULTILINE)

    # Using for loop for retrieve and surf on file features
    for iterationFile in text_files:
        text = Path(iterationFile).read_text()
        # Rewrite the existing filename
        with open(iterationFile, mode='w', encoding="utf-8") as outfile:
            new_file = re.sub(words_to_replace, replace_words_using_dict, text)
            outfile.write(new_file)
else:
    while value.lower() not in ("y", "n"):
        value = input("Another one? y/n > ")
        if value == "n":
            print("Break, because you have not edited csv file")
            break
