# Author: Tan Huynh
# Team : LMI-Testautomat
# Branch Convention for Gitlab with Hyphenation

import json
import re
from jira import JIRA, JIRAError
from atlassian import Jira

jira = Jira(
    url='YOUR_URL_JIRA_SERVER',
    username='YOUR_JIRA_USERNAME',
    password='YOUR_JIRA_PASSWORD')

name = input('Ticketnumer for Gitlab Branch Name Convention?\n')
try:   
    issue = jira.issue(name.upper())
except  Exception as e:
    print(e)
    exit(1)

# extract json file from jira response
s1 = json.dumps(issue)
ptrElementFields = json.loads(s1)

fields = ptrElementFields["fields"]
s2 = json.dumps(fields)
ptrElementDescription = json.loads(s2)

issuetype = ptrElementDescription["issuetype"]
s3 = json.dumps(issuetype)
ptrElementIssue = json.loads(s3)

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

lowerCaseSummary = ptrElementDescription["summary"].lower()

# replace non-words in ticket summary
d = {".": "", \
     ":": "", \
     ",": "", \
     "-": "", \
     '\"': "", \
     '\'': "", \
     "?": "", \
     }
lowerCaseSummaryPostProcess = replace_all(lowerCaseSummary, d)
connectWordsInSummary = lowerCaseSummaryPostProcess.replace(' ', '-')

# consider type of ticket
typeOfTicket = ptrElementIssue["name"].lower()
listTicketTypes = {"story": "feature", \
                   "bug": "bugfix" \
                  }
typeOfTicketPostProcess = replace_all(typeOfTicket, listTicketTypes)

result = '{}/{}-{}'.format(typeOfTicketPostProcess, ptrElementFields["key"], connectWordsInSummary)
result2 = re.sub('\-{2,}', ' ', result)
result3 = result2.replace(' ', '-')
print(result3)            # 'JIRA'
