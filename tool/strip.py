import json
import os


CHUNK_SIZE = 100


def strip_course(courses_list: list[dict], output_dir: str, output_file_prefix: str = "courses_"):
    # === 輸出分段檔案 ===
    os.makedirs(output_dir, exist_ok=True)

    for i in range(0, len(courses_list), CHUNK_SIZE):
        chunk = courses_list[i:i+CHUNK_SIZE]
        path = os.path.join(
            output_dir, f"{output_file_prefix}_{i//CHUNK_SIZE+1}.min.json")
        with open(path, "w", encoding="utf-8") as out:
            json.dump(chunk, out, ensure_ascii=False, separators=(",", ":"))

    file_num = (len(courses_list)-1)//CHUNK_SIZE+1
    with open(os.path.join(output_dir, f"{output_file_prefix}_0.min.json"), "w", encoding="utf-8") as out:
        json.dump({"total": file_num}, out,
                  ensure_ascii=False, separators=(",", ":"))
    print(f"✅ 完成輸出：{file_num} 個檔案 → {output_dir}")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if args:
        if len(args) == 3:
            original_data_path = os.path.abspath(args[0])
            output_dir = os.path.abspath(args[1])
            output_prefix = args[2]
        else:
            print("[!] 參數格式錯誤")
            sys.exit(1)
    else:
        original_data_path = input("original data path:")
        output_dir = input("output dir:")
        output_prefix = input("output prefix:")
    if not os.path.isfile(original_data_path):
        print(f"⚠️ 檔案格式錯誤：{original_data_path}")
        sys.exit(1)
    if not os.path.exists(output_dir):
        print(f"⚠️ 資料夾不存在：{output_dir}")
        os.makedirs(output_dir)
    with open(original_data_path, "r", encoding="utf-8") as f:
        courses = json.load(f)
    strip_course(courses, output_dir, output_prefix)
    print(f"✔️ 完成處理：{len(courses)} 筆課程資料")
