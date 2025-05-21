import json
import os


def strip_course(courses_list: list[dict], output_dir: str):
    # === 輸出分段檔案 ===
    os.makedirs(output_dir, exist_ok=True)

    files = {f"{i}.min.json": [] for i in range(0, 10)}

    for course in courses_list:
        serial_no: str = course.get("serial_no")
        # e.g., '1234' -> '2.min.json', '8000' -> '9.min.json'
        if serial_no is not None and len(serial_no) == 4:
            try:
                file_key = f"{int(serial_no[0]) + 1}.min.json"
            except ValueError:
                file_key = "0.min.json"
        else:
            file_key = "0.min.json"

        if file_key not in files:
            files[file_key] = []

        files[file_key].append(course)

    for file_key, data in files.items():
        path = os.path.join(output_dir, file_key)
        with open(path, "w", encoding="utf-8") as out:
            json.dump(data, out, ensure_ascii=False, separators=(",", ":"))

    print(f"✅ 完成輸出：{len(files)} 個檔案 → {output_dir}")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if args:
        if len(args) == 2:
            original_data_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "original_data",
                f"{args[0]}-{args[1]}_format.json"))
            output_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "..",
                "frontend", "public", "data", f"{args[0]}-{args[1]}"))
        else:
            print("[!] 參數格式錯誤")
            sys.exit(1)
    else:
        original_data_path = input("original data path:")
        output_dir = input("output dir:")
    if not os.path.isfile(original_data_path):
        print(f"⚠️ 檔案格式錯誤：{original_data_path}")
        sys.exit(1)
    if not os.path.exists(output_dir):
        print(f"⚠️ 資料夾不存在：{output_dir}")
        os.makedirs(output_dir)
    with open(original_data_path, "r", encoding="utf-8") as f:
        courses = json.load(f)
    strip_course(courses, output_dir)
    print(f"✔️ 完成處理：{len(courses)} 筆課程資料")
