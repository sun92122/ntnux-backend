import time
import sys
import os
import json

from crawl.browser import trigger_course_requests
from tool.proxy import run_mitmproxy
from tool.parse import parse_course


def main(year: int, term: int | str):
    print("[*] 啟動 mitmproxy 攔截器...")
    mitm_proc = run_mitmproxy()
    time.sleep(3)  # 等待 proxy 啟動

    # check if mitmproxy is running
    if mitm_proc.poll() is not None:
        print("[!] mitmproxy 啟動失敗")
        return
    print("[*] mitmproxy 啟動成功，PID:", mitm_proc.pid)

    print("[*] 開始 Selenium 自動操作...")
    try:
        trigger_course_requests(year, term)
    finally:
        print("[*] 結束 mitmproxy")
        mitm_proc.terminate()

    raw_data_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "data", "response_content.json"))
    course_datas = parse_course(raw_data_path)
    original_data_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "original_data", f"{year}-{term}.json"))
    with open(original_data_path, "w", encoding="utf-8") as f:
        json.dump(course_datas, f, ensure_ascii=False, separators=(",", ": "))
    print(f"✔️ 完成處理 {year}-{term} 的課程資料，已儲存至 {original_data_path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        if len(args) == 2:  # 112 1, 113 2, 111 暑
            args = tuple(int(i) if i.isdigit() else i for i in args)
            print("[*] 使用自訂參數：", args, sep="")
        if len(args) == 1:  # 112-1, 113-2, ...
            try:
                args = tuple(int(i) if i.isdigit()
                             else i for i in args[0].split("-"))
            except ValueError:
                print("[!] 參數格式錯誤")
                sys.exit(1)
    else:
        args = (113, 2)
        print("[*] 使用預設參數：", args, sep="")
    main(*args)
