import json
import os


CHUNK_SIZE = 100


def parse_course(original_data_path: str, output_dir: str, output_file_prefix: str = "courses_"):
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

    print(f"✔️ 共保留課程數：{len(all_courses)}")

    # === 輸出分段檔案 ===
    os.makedirs(output_dir, exist_ok=True)

    for i in range(0, len(all_courses), CHUNK_SIZE):
        chunk = all_courses[i:i+CHUNK_SIZE]
        path = os.path.join(
            output_dir, f"{output_file_prefix}{i//CHUNK_SIZE+1}.min.json")
        with open(path, "w", encoding="utf-8") as out:
            json.dump(chunk, out, ensure_ascii=False, separators=(",", ":"))

    file_num = (len(all_courses)-1)//CHUNK_SIZE+1
    with open(os.path.join(output_dir, f"{output_file_prefix}0.min.json"), "w", encoding="utf-8") as out:
        json.dump({"total": file_num}, out, ensure_ascii=False, separators=(",", ":"))
    print(f"✅ 完成輸出：{file_num} 個檔案 → {output_dir}")


def main():
    original_data_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "../data/response_content.json"))
    output_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "../../frontend/public/data"))
    output_prefix = "113-2_"
    if not os.path.exists(original_data_path):
        print(f"⚠️ 檔案不存在：{original_data_path}")
        return
    parse_course(original_data_path, output_dir, output_prefix)


if __name__ == "__main__":
    main()
