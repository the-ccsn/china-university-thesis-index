import json
from functools import cmp_to_key

syntax_1 = "<!-- MARKDOWN_TABLE BEGIN -->"
syntax_2 = "<!-- WARNING: THIS TABLE IS MAINTAINED BY PROGRAMME, YOU SHOULD ADD DATA TO COLLECTION JSON -->"
syntax_3 = "<!-- MARKDOWN_TABLE END -->"


def x_sort(data):
    def compare(dict_a: dict, dict_b: dict):
        dict_a_packagename = (
            dict_a["package_name"].replace("_", "").replace("-", "").lower()
        )
        dict_b_packagename = (
            dict_b["package_name"].replace("_", "").replace("-", "").lower()
        )
        dict_a_ctan = dict_a["ctan_package"]
        dict_b_ctan = dict_b["ctan_package"]
        if dict_a_ctan == "" and dict_b_ctan == "":
            if dict_a_packagename < dict_b_packagename:
                return -1
            if dict_a_packagename > dict_b_packagename:
                return 1
        elif dict_a_ctan == "" and dict_b_ctan != "":
            return 1
        elif dict_b_ctan == "" and dict_a_ctan != "":
            return -1
        else:
            if dict_a_packagename < dict_b_packagename:
                return -1
            if dict_a_packagename > dict_b_packagename:
                return 1

    data = sorted(data, key=cmp_to_key(compare))
    return data


def badge(link: str, maintainer_type="组织", badge_type="github") -> str:
    host = ["github", "gitlab", "gitee", "gitea"]
    if link == "":
        return link
    if badge_type in host:
        link_template = "https://img.shields.io/badge/{{user_name}}%2F{{repo_name}}-{{color}}?logo={{badge_type}}&link=https%3A%2F%2Fgithub.com%2F{{user_name}}%2F{{repo_name}}"
        user_name = link.split("/")[1].replace("-", "--")
        repo_name = link.split("/")[2].replace("-", "--")
        if maintainer_type == "组织" or maintainer_type == "orgs":
            link_template = link_template.replace("{{color}}", "blue")
        elif maintainer_type == "个人" or maintainer_type == "user":
            link_template = link_template.replace("{{color}}", "green")
        else:
            link_template = link_template.replace("{{color}}", "red")
        link_template = (
            link_template.replace("{{user_name}}", user_name)
            .replace("{{repo_name}}", repo_name)
            .replace("{{badge_type}}", badge_type)
        )
        return "![](" + link_template + ")"
    elif badge_type == "ctan":
        link_template = "https://img.shields.io/badge/ctan-{{thesis}}-lightgray?link=https%3A%2F%2Fctan.org%2Fpkg%2F{{thesis}}"
        thesis_name = link.replace("ctan.org/pkg/", "")
        link_template = link_template.replace("{{thesis}}", thesis_name)
        return "![](" + link_template + ")"
    else:
        return link


def repos(
    maintainer_type: str,
    repository_github: str,
    repository_gitlab: str,
    repository_gitee: str,
    repository_gitea: str,
):
    repo_cell_template = "<div>{{repo_list}}</div>"
    repo_list = []
    if repository_github != "":
        repo_list.append(
            "<b>GitHub:</b><br/>"
            + badge(
                link=repository_github,
                maintainer_type=maintainer_type,
                badge_type="github",
            )
        )
    if repository_gitlab != "":
        repo_list.append(
            "<b>GitLab Official:</b><br/>"
            + badge(
                link=repository_gitlab,
                maintainer_type=maintainer_type,
                badge_type="gitlab",
            )
        )
    if repository_gitee != "":
        repo_list.append(
            "<b>Gitee:</b><br/>"
            + badge(
                link=repository_gitee,
                maintainer_type=maintainer_type,
                badge_type="gitee",
            )
        )
    if repository_gitea != "":
        repo_list.append(
            "<b>Gitea Official:</b><br/>"
            + badge(
                link=repository_gitea,
                maintainer_type=maintainer_type,
                badge_type="gitea",
            )
        )

    return repo_cell_template.replace("{{repo_list}}", "<br/>".join(repo_list))


def markdown_row(data: list):
    string = ""
    for i in data:
        string += "| " + i + " "
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
        locale_translation["repository"],
        locale_translation["ctan_package"],
        locale_translation["status"],
    ]
    return markdown_row(data)


def markdown_table(length: int):
    data = ["-", "-", "-", "-", "-", "-"]
    return markdown_row(data)


def markdown_entry(thesis_entry: dict):
    data = [
        thesis_entry["package_name"],
        thesis_entry["institution_name"],
        thesis_entry["maintainer_type"],
        repos(
            maintainer_type=thesis_entry["maintainer_type"],
            repository_github=thesis_entry["repository_github"],
            repository_gitlab=thesis_entry["repository_gitlab"],
            repository_gitee=thesis_entry["repository_gitee"],
            repository_gitea=thesis_entry["repository_gitea"],
        ),
        badge(
            link=thesis_entry["ctan_package"],
            badge_type="ctan",
        ),
        thesis_entry["status"],
    ]
    return markdown_row(data)


def markdown_gen(locale: str):
    thesis_json = open("..\\data\\thesis.json", "r", encoding="utf-8")
    thesis_data = json.loads(thesis_json.read())["CUTI"]
    column_json = open("..\\data\\column.json", "r", encoding="utf-8")
    column_data = json.loads(column_json.read())
    string = ""
    if locale != "Default":
        string += markdown_header(column_data["i18n"], locale)
    else:
        string += markdown_header(column_data["i18n"], "zh-CN")
    string += markdown_table(
        column_data["len"],
    )
    # WRONG CODE: thesis_data.sort(key=lambda x: x["package_name"])
    thesis_data = x_sort(thesis_data)
    for i in range(len(thesis_data)):
        string += markdown_entry(thesis_data[i])
    return string


def markdown_body(locale, text, token_begin, token_warn, token_end):
    readme_slice = text.split(token_begin)
    readme_slice.append(readme_slice[1].split(token_warn)[0])
    readme_slice.append(readme_slice[1].split(token_end)[1])
    table = markdown_gen(locale)
    markdown = (
        readme_slice[0]
        + token_begin
        + "\n"
        + token_warn
        + "\n"
        + table
        + "\n"
        + token_end
        + readme_slice[3]
    )
    if table == "":
        return text
    else:
        return markdown


def readme_gen(readme_locale):
    if readme_locale != "":
        path = "..\\README" + "-" + readme_locale + ".md"
    else:
        readme_locale = "Default"
        path = "..\\README.md"
    readme_file = open(path, "r", encoding="utf-8")
    readme_text = readme_file.read()
    readme_file.close()
    readme_text = markdown_body(
        readme_locale, readme_text, syntax_1, syntax_2, syntax_3
    )
    readme_file = open(path, "w", encoding="utf-8")
    readme_file.write(readme_text)
    readme_file.close()
    print(readme_locale, ": ", path.replace("..\\", "").replace("../", ""))


readme_gen("")
readme_gen("zh-CN")
readme_gen("en-US")
