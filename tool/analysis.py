import pandas as pd


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


def course_format(courses: pd.DataFrame) -> pd.DataFrame:
    """
    將課程資訊 DataFrame 格式化為指定的格式
    :param courses: 課程資訊 DataFrame
    :return: 格式化後的課程資訊 DataFrame
    """
    courses["generalCore"] = courses["generalCore"].fillna("")
    return courses[[
        "acadm_year", "acadm_term", "authorize_p", "authorize_using",
        "chn_name", "classes", "comment", "counter", "counter_exceptAuth",
        "course_avg", "course_code", "course_group", "course_kind", "credit",
        "dept_chiabbr", "dept_code", "dept_group_name", "eng_name",
        "eng_teach", "form_s", "limit", "limit_count_h", "option_code",
        "restrict", "rt", "serial_no", "teacher", "time_inf",
        "generalCore"
    ]]
