import json


def parse_course(original_data_path: str):
    with open(original_data_path, "r", encoding="utf-8") as f:
        raw_blocks = json.load(f)

    all_courses = []
    seen = {}

    for block in raw_blocks:
        for course in block.get("List", []):
            serial = course.get("serial_no", "").strip()

            if not serial:  # 空的 serial_no 允許重複加入
                all_courses.append(course)
                continue

            if serial in seen:
                if seen[serial] != course:
                    print(
                        f"⚠️ Warning: Duplicate serial_no '{serial}' found with different data.")
                # 若相同就略過，不再加入
                continue
            else:
                seen[serial] = course
                all_courses.append(course)
    
    # 依照 serial_no 排序
    all_courses = sorted(all_courses, key=lambda x: x.get("serial_no", "").strip())

    print(f"✔️ 共保留課程數：{len(all_courses)}")
    return all_courses
