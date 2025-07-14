import time
import argparse
import requests
import json

BASE = "https://courseap2.itc.ntnu.edu.tw"
INDEX_URL = f"{BASE}/acadmOpenCourse/index.jsp"
API_URL = f"{BASE}/acadmOpenCourse/CofopdlCtrl"
DEPT_API_URL = f"{BASE}/acadmOpenCourse/CofnameCtrl"
GU_CORE = ['A1UG', 'A2UG', 'A3UG', 'A4UG',
           'B1UG', 'B2UG', 'B3UG', 'C1UG', 'C2UG']


def build_params(year: int, term: int, dept: str, limit: int = 99999):
    """組出 GET 參數 dict"""
    return {
        "_dc": int(time.time() * 1000),  # 避免快取
        "acadmYear": year,
        "acadmTerm": term,
        "deptCode": dept,
        "action": "showGrid",
        "language": "chinese",
        "start": 0,
        "limit": limit,
        "page": 1,
        # 其餘過濾條件全留空或 N
        "chn": "", "engTeach": "N", "clang": "N",
        "moocs": "N", "remoteCourse": "N", "digital": "N",
        "adsl": "N", "zuDept": "", "classCode": "", "kind": "",
        "generalCore": "", "teacher": "", "serial_number": "",
        "course_code": "",
    }


def build_dept_params(year: int, term: int, limit: int = 25):
    """組出科系列表的 GET 參數 dict"""
    return {
        "_dc": int(time.time() * 1000),  # 避免快取
        "action": "cof",
        "type": "chn",
        "year": year,
        "term": term,
        "page": 1,
        "start": 0,
        "limit": limit,
    }


def fetch_courses(year: int, term: int, depts: list[str] = None):
    all_courses = []
    with requests.Session() as s:
        # 1. 造訪 index.jsp 取得 JSESSIONID
        s.get(INDEX_URL, timeout=10)

        headers = {
            "Referer": INDEX_URL,
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
            "Accept-Language": "zh-TW,zh;q=0.9",
        }

        # 2. 取得科系列表
        depts_original = []
        if depts is None:
            resp = s.get(DEPT_API_URL,
                         headers=headers,
                         params=build_dept_params(year, term))
            resp.raise_for_status()
            depts_original = json.loads(resp.text.replace("'", '"'))
            depts = [item[0] for item in depts_original]
            print(f"共取得 {len(depts)} 個科系代碼")

        for i, dept in enumerate(depts):
            try:
                print(f"正在抓取 {depts_original[i][1]} 的課程資料...")
            except IndexError:
                print(f"正在抓取 {dept} 的課程資料...")

            if dept == "GU":
                for core in GU_CORE:
                    time.sleep(0.5)
                    resp = s.get(API_URL,
                                 headers=headers,
                                 params=build_params(year, term, "GU") |
                                 {"kind": 3, "generalCore": core})
                    resp.raise_for_status()
                    data = resp.json().get("List", [])
                    # 對所有 data 內容:
                    # 尋找 all_courses 中是否已存在相同 serial_no 的課程
                    # 有 -> 對其 generalCore 欄位修改加 "/core"，若原本為空則 改為 core
                    # 沒有 -> 直接加入 all_courses，並將 generalCore 設為 core
                    # 沒有 serial_no: 改用 (courseCode, courseGroup) 作為唯一識別
                    for course in data:
                        serial_no = course.get("serial_no")
                        if serial_no:
                            existing = next(
                                (c for c in all_courses
                                 if c["serial_no"] == serial_no), None)
                            if existing:
                                if core not in existing["generalCore"]:
                                    existing["generalCore"] += f"/{core}"
                            else:
                                course["generalCore"] = core
                                all_courses.append(course)
                        else:
                            # 處理沒有 serial_no 的情況
                            existing = next(
                                (c for c in all_courses
                                 if (c["course_code"] == course["course_code"] and
                                     c["course_group"] == course["course_group"])), None)
                            if existing:
                                if core not in existing["generalCore"]:
                                    existing["generalCore"] += f"/{core}"
                            else:
                                course["generalCore"] = core
                                all_courses.append(course)
                continue
            time.sleep(0.5)
            resp = s.get(API_URL,
                         headers=headers,
                         params=build_params(year, term, dept))
            resp.raise_for_status()
            data = resp.json().get("List", [])
            all_courses.extend(data)

        # 移除重複課程（serial_no 相同，沒有 serial_no: 改用 (courseCode, courseGroup) 作為唯一識別）
        seen_serials = set()

        def seen_serials_add(course):
            serial_no = course.get("serial_no")
            if serial_no:
                return serial_no not in seen_serials and not seen_serials.add(serial_no)
            else:
                unique_key = (course["course_code"], course["course_group"])
                return unique_key not in seen_serials and not seen_serials.add(unique_key)

        all_courses = [course for course in all_courses
                       if seen_serials_add(course)]
    return all_courses


def fetch_course(year: int, term: int, dept: str):
    with requests.Session() as s:
        # 1. 造訪 index.jsp 取得 JSESSIONID
        s.get(INDEX_URL, timeout=10)

        # 2. API 呼叫
        headers = {
            "Referer": INDEX_URL,
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
            "Accept-Language": "zh-TW,zh;q=0.9",
        }
        resp = s.get(API_URL,
                     headers=headers,
                     params=build_params(year, term, dept))
        resp.raise_for_status()
        data = resp.json().get("List", [])
        return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y","--year", type=int, required=True, help="民國學年度，如 113")
    parser.add_argument("-t","--term", type=int, required=True, help="學期：1 、 2 或 3")
    parser.add_argument("-d","--dept", type=str, help="科系代碼，如 AIA")
    parser.add_argument("-o", "--out", type=str, default=None,
                        help="TSV 輸出檔名，可省略")
    args = parser.parse_args()

    if args.dept:
        data = fetch_course(args.year, args.term, args.dept)
    else:
        # data = fetch_courses(args.year, args.term)
        data = fetch_courses(args.year, args.term, ["GU"])
        args.out = f"{args.year}-{args.term}.tsv"
    import pandas as pd
    df = pd.DataFrame(data)
    print(f"抓到 {len(df)} 筆課程資料")
    print(df.head(10))  # 顯示前 10 筆資料
    if args.out:
        df.to_csv(args.out, index=False, sep="\t", encoding="utf-8-sig")
        print(f"已輸出 {args.out}")


if __name__ == "__main__":
    main()
