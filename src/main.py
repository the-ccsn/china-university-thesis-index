import json

def markdown_header():
    pass

def markdown_table():
    pass

def markdown_entry():
    pass

json_file= open("..\\data\\thesis.json", "r", encoding="utf-8")
data=json.loads(json_file.read())["CUTI"]
tmp=""
tmp+=markdown_header()
tmp+=markdown_table()
for i in range(len(data)):
    tmp+=markdown_entry(data[i])