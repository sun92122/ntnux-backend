import os
import json
from mitmproxy import http

DATA_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../data/response_content.json"))

# 初始化檔案
with open(DATA_PATH, "w", encoding="utf-8") as f:
    f.write("[]")


def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url.startswith(
        "https://courseap2.itc.ntnu.edu.tw/acadmOpenCourse/CofopdlCtrl?_dc="
    ):
        try:
            text = flow.response.get_text()
            new_data = json.loads(text)
            with open(DATA_PATH, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(new_data)
                f.seek(0)
                f.write(json.dumps(data, ensure_ascii=False, indent=4))
                f.truncate()
        except Exception as e:
            print(f"解析或寫入錯誤: {e}")
            # save text to file for debugging
            with open("debug.txt", "a", encoding="utf-8") as debug_file:
                debug_file.write(text)
