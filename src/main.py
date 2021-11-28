import json


def x_sort(data):
    def compare(dict_a:dict, dict_b:dict):
        dict_a_packagename = dict_a["package_name"].replace("_","").replace("-","").lower()
        dict_b_packagename = dict_b["package_name"].replace("_","").replace("-","").lower()
        dict_a_ctan=dict["ctan"]
        dict_b_ctan=dict["ctan"]
        if dict_a_ctan is "":
            return -1
        elif dict_b_ctan is "":
            return 1
        else:
            if dict_a_packagename < dict_b_packagename:
                return -1
            if dict_a_packagename > dict_b_packagename:
                return 1
    data.sort(compare)
    return data


def markdown_row(length: int, data: list):
    string = ""
    for i in range(length):
        string += "| " + str(data[i]) + " "
    string += "|\n"
    return string


def markdown_header(translation: dict, locale: str):
    locale_translation = {}
    for i in range(len(translation)):
        if translation[i]["locale"] == locale:
            locale_translation = translation[i]["translation"]
    data = [
        locale_translation["package_name"],
        locale_translation["institution_name"],
        locale_translation["maintainer_type"],
        locale_translation["github_repository"],
        locale_translation["gitlab_repository"],
        locale_translation["gitee_repository"],
        locale_translation["ctan_package"],
        locale_translation["status"],
    ]
    return markdown_row(len(data), data)


def markdown_table(length: int):
    data = ["-", "-", "-", "-", "-", "-", "-", "-"]
    return markdown_row(length, data)


def markdown_entry(thesis_entry: dict):
    data = [
        thesis_entry["package_name"],
        thesis_entry["institution_name"],
        thesis_entry["maintainer_type"],
        thesis_entry["github_repository"],
        thesis_entry["gitlab_repository"],
        thesis_entry["gitee_repository"],
        thesis_entry["ctan_package"],
        thesis_entry["status"],
    ]
    return markdown_row(len(data), data)


def markdown_gen():
    thesis_json = open("..\\data\\thesis.json", "r", encoding="utf-8")
    thesis_data = json.loads(thesis_json.read())["CUTI"]
    column_json = open("..\\data\\column.json", "r", encoding="utf-8")
    column_data = json.loads(column_json.read())
    string = ""
    string += markdown_header(column_data["i18n"], "zh-CN")
    string += markdown_table(
        column_data["len"],
    )
    # WRONG CODE: thesis_data.sort(key=lambda x: x["package_name"])
    thesis_data = x_sort(thesis_data)
    for i in range(len(thesis_data)):
        string += markdown_entry(thesis_data[i])
    return string


def markdown_body(text, token_begin, token_warn, token_end):
    readme_slice = text.split(token_begin)
    readme_slice.append(readme_slice[1].split(token_warn)[0])
    readme_slice.append(readme_slice[1].split(token_end)[1])
    markdown = (
        readme_slice[0]
        + token_begin
        + "\n"
        + token_warn
        + "\n"
        + markdown_gen()
        + "\n"
        + token_end
        + readme_slice[3]
    )
    if markdown_gen() is "":
        return text
    else:
        return markdown


syntax_1 = "<!-- MARKDOWN_TABLE BEGIN -->"
syntax_2 = "<!-- WARNING: THIS TABLE IS MAINTAINED BY PROGRAMME, YOU SHOULD ADD DATA TO COLLECTION JSON -->"
syntax_3 = "<!-- MARKDOWN_TABLE END -->"
readme_file = open("..\\README.md", "r", encoding="utf-8")
readme_text = readme_file.read()
readme_file.close()
readme_file = open("..\\README.md", "w", encoding="utf-8")
readme_file.write(markdown_body(readme_text, syntax_1, syntax_2, syntax_3))
readme_file.close()
