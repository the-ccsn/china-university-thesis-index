import json

def markdown_row(len:int,data:list):
    string=""
    for i in range(len):
        string+="| "+str(data[i])+" "
    string+="|\n"
    return string

def markdown_header(translation:dict,locale:str):
    locale_translation={}
    for i in range(len(translation)):
        if translation[i]["locale"] == locale:
            locale_translation=translation[i]["translation"]
    data= [locale_translation["package_name"], locale_translation["institution_name"],
           locale_translation["maintainer_type"], locale_translation["github_repository"],
           locale_translation["gitlab_repository"], locale_translation["gitee_repository"],
           locale_translation["ctan_package"], locale_translation["status"]]
    return markdown_row(len(data),data)


def markdown_table(length:int):
    data=["-","-","-","-","-","-","-","-"]
    return markdown_row(length,data)

def markdown_entry(thesis_entry:dict):
    data=[
        thesis_entry["package_name"],
        thesis_entry["institution_name"],
        thesis_entry["maintainer_type"],
        thesis_entry["github_repository"],
        thesis_entry["gitlab_repository"],
        thesis_entry["gitee_repository"],
        thesis_entry["ctan_package"],
        thesis_entry["status"]
    ]
    return markdown_row(len(data),data)

thesis_json= open("..\\data\\thesis.json", "r", encoding="utf-8")
thesis_data=json.loads(thesis_json.read())["CUTI"]
column_json= open("..\\data\\column.json", "r", encoding="utf-8")
column_data=json.loads(column_json.read())
tmp=""
tmp+=markdown_header(column_data["i18n"],"zh-CN")
tmp+=markdown_table(column_data["len"],)
for i in range(len(thesis_data)):
    tmp+=markdown_entry(thesis_data[i])
print(tmp)