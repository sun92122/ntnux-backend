import os
import json
from mitmproxy import http

DATA_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../data/response_content.json"))

# 初始化檔案
with open(DATA_PATH, "w", encoding="utf-8") as f:
    f.write("[]")
counter = 0


def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url.startswith(
        "https://courseap2.itc.ntnu.edu.tw/acadmOpenCourse/CofopdlCtrl?_dc="
    ):
        try:
            text = flow.response.get_text()
            new_data = json.loads(text)

            general_core = flow.request.query.get("generalCore")
            if general_core:
                for item in new_data['List']:
                    item["generalCore"] = [general_core,]

            with open(DATA_PATH, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(new_data)
                f.seek(0)
                f.write(json.dumps(data, ensure_ascii=False))
                f.truncate()
            global counter
            counter += 1
            print(f"✔️ 已儲存第 {counter} 筆資料")
        except Exception as e:
            print(f"解析或寫入錯誤: {e}")
            # save text to file for debugging
            with open(
                os.path.abspath(os.path.join(
                    os.path.dirname(__file__), "../debug.log")),
                    "a", encoding="utf-8") as debug_file:
                debug_file.write(f"Error: {e}\n")
                debug_file.write(f"Request URL: {flow.request.pretty_url}")
