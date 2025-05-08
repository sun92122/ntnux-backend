# 原始格式
# {
#     "acadm_term": "1",
#     "acadm_year": "112",
#     "authorize_p": "0",
#     "authorize_r": "0.00",
#     "authorize_using": "0",
#     "brief_eng": "",
#     "cancel": "",
#     "chn_name": "西洋古典音樂",
#     "class_name": "",
#     "classes": "",
#     "comment": "",
#     "counter": "44",
#     "counter_exceptAuth": "44",
#     "course_avg": "",
#     "course_code": "01UG003",
#     "course_group": "",
#     "course_kind": "半",
#     "credit": "2.0",
#     "deleteQ": "",
#     "dept_chiabbr": "通識",
#     "dept_code": "GU",
#     "dept_engfull": "",
#     "dept_group": "",
#     "dept_group_name": "",
#     "emi": "",
#     "eng_name": "Classical Music",
#     "eng_teach": "是",
#     "exp_hours": "",
#     "fillcounter": "",
#     "for_query": "",
#     "form_s": "",
#     "form_s_name": "",
#     "full_flag": "",
#     "gender_restrict": "",
#     "hours": "",
#     "iCounter": "",
#     "intensive": "",
#     "limit": "0",
#     "limit_count_h": "50",
#     "moocs_teach": "",
#     "not_choose": "",
#     "option_code": "通",
#     "percentage": "",
#     "restrict": "◎音樂系（學）不得選修",
#     "rt": "N",
#     "school_avg": "",
#     "scoreEnt": "",
#     "selfTeach": "",
#     "selfTeachName": "",
#     "send_time": "",
#     "serial_no": "0885",
#     "status": "",
#     "tcode": "",
#     "teacher": "劉思涵",
#     "time_inf": "四 8-9 公館 Ｂ102",
#     "tname": "",
#     "umd": "",
#     "week_section1": "",
#     "week_section2": "",
#     "week_section3": "",
#     "week_section4": ""
# },

# 格式化後
# {
#     acadm_term: "1",
#     acadm_year: "112",
#     authorize_p: "0",
#     authorize_using: "0",
#     chn_name: "西洋古典音樂",
#     classes: "",
#     comment: "",
#     counter: "44",
#     counter_exceptAuth: "44",
#     course_avg: "",
#     course_code: "01UG003",
#     course_group: "",
#     course_kind: "半",
#     credit: "2.0",
#     dept_chiabbr: "通識",
#     dept_code: "GU",
#     dept_group_name: "",
#     eng_name: "Classical Music",
#     eng_teach: "是",
#     form_s: "",
#     limit: "0",
#     limit_count_h: "50",
#     option_code: "通",
#     restrict: "◎音樂系（學）不得選修",
#     rt: "N",
#     serial_no: "0885",
#     teacher: "劉思涵",
#     time_inf: "四 8-9 公館 Ｂ102",
#     time_loc: { "四 8-9": "公館 Ｂ102" },
# }

import json


def time_location_format(time_inf: str) -> dict[str, str] | str:
    """
    將時間地點資訊格式化為指定的格式
    :param time_inf: 原始時間資訊
    :return: 格式化後的時間、地點資訊
    """
    if not time_inf or time_inf.startswith('◎'):
        return time_inf

    time_loc_parts = time_inf.split(",")
    formatted_times = {}
    for part in time_loc_parts:
        # 提取星期和時間
        part = part.strip().split(" ")
        day_time = part[0:2]
        location = part[2:]
        if len(day_time) == 2:
            formatted_times[" ".join(day_time)] = " ".join(location)
    # 返回格式化後的時間資訊
    return formatted_times


def course_format(course: json) -> dict:
    """
    將課程資訊格式化為指定的格式
    :param course: 課程資訊
    :return: 格式化後的課程資訊
    """
    return {
        "acadm_year": course["acadm_year"],
        "acadm_term": course["acadm_term"],
        "authorize_p": course["authorize_p"],
        "authorize_using": course["authorize_using"],
        "chn_name": course["chn_name"],
        "classes": course["classes"],
        "comment": course["comment"],
        "counter": course["counter"],
        "counter_exceptAuth": course["counter_exceptAuth"],
        "course_avg": course["course_avg"],
        "course_code": course["course_code"],
        "course_group": course["course_group"],
        "course_kind": course["course_kind"],
        "credit": course["credit"],
        "dept_chiabbr": course["dept_chiabbr"],
        "dept_code": course["dept_code"],
        "dept_group_name": course["dept_group_name"],
        "eng_name": course["eng_name"],
        "eng_teach": course["eng_teach"],
        "form_s": course["form_s"],
        "limit": course["limit"],
        "limit_count_h": course["limit_count_h"],
        "option_code": course["option_code"],
        "restrict": course["restrict"],
        "rt": course["rt"],
        "serial_no": course["serial_no"],
        "teacher": course["teacher"],
        "time_inf": course["time_inf"],
        "time_loc": time_location_format(course["time_inf"]),
        "generalCore": course.get("generalCore", []),
    }


def course_format_list(courses: list) -> list:
    """
    將課程資訊列表格式化為指定的格式
    :param courses: 課程資訊列表
    :return: 格式化後的課程資訊列表
    """
    return [course_format(course) for course in courses]


if __name__ == '__main__':
    import os
    import sys

    args = sys.argv[1:]
    if args:
        if len(args) == 1:  # 112-1, 113-2, ...
            original_data_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "original_data",
                f"{args[0]}.json"))
            format_data_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "original_data",
                f"{args[0]}_format.json"))
        elif len(args) == 2:  # 112 1, 113 2, 111 3
            original_data_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "original_data",
                f"{args[0]}-{args[1]}.json"))
            format_data_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "original_data",
                f"{args[0]}-{args[1]}_format.json"))
        else:
            print("[!] 參數格式錯誤")
            sys.exit(1)
    else:
        original_data_path = input("original data path:")
        format_data_path = input("format data path:")

    data = []
    with open(original_data_path, 'r', encoding='utf-8') as f:
        data.extend(json.load(f))

    # 只保留需要的欄位
    data = course_format_list(data)

    # 將格式化後的資料寫入新的 JSON 檔案
    with open(format_data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        print("格式化完成，資料已寫入", f.name)
