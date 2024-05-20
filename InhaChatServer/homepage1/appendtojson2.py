import json
import os

def write_json_inha_notice(page, filename="인하대학교 테스트.json",):
    with open(filename, "r+", encoding="utf-8") as file:
        file_content = json.load(file)
        file_content["인하대학교_테스트"].append(page)
        file.seek(0)
        json.dump(file_content, file, ensure_ascii=False, indent=4)
def write_json_everytime(page, filename="everytime2024y.json",):
    with open(filename, "r+", encoding="utf-8") as file:
        file_content = json.load(file)
        file_content["everytime"].append(page)
        file.seek(0)
        json.dump(file_content, file, ensure_ascii=False, indent=4)
