import json

def write_json(page, filename="everytime2021.json",):
    with open(filename, "r+", encoding="utf-8") as file:
        file_content = json.load(file)
        file_content["everytime"].append(page)
        file.seek(0)
        json.dump(file_content, file, ensure_ascii=False, indent=4)

if __name__=='__main__':
    everytime = {
        "Question": "과잠 바꾸실 분?",
        "Answer":
            {
                "answer1": "경영학과인데 l사이즈라 안타깝네요.. 전과할 수 있는 기회였는데",
                "answer2": "학잠 xl인데 치수 크게 나온거 ㄱㅊ으신가요??",
                "answer3": "디텍 과잠 2xl랑 바꾸실래요?",
            }
    }

    write_json(everytime)