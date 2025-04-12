import time

from crawl.browser import trigger_course_requests
from tool.proxy import run_mitmproxy


def main():
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
        trigger_course_requests()
    finally:
        print("[*] 結束 mitmproxy")
        mitm_proc.terminate()


if __name__ == "__main__":
    main()
