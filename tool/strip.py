import json
import os


CHUNK_SIZE = 100


def strip_course(courses_list: list[dict], output_dir: str, output_file_prefix: str = "courses_"):
    # === 輸出分段檔案 ===
    os.makedirs(output_dir, exist_ok=True)

    for i in range(0, len(courses_list), CHUNK_SIZE):
        chunk = courses_list[i:i+CHUNK_SIZE]
        path = os.path.join(
            output_dir, f"{output_file_prefix}{i//CHUNK_SIZE+1}.min.json")
        with open(path, "w", encoding="utf-8") as out:
            json.dump(chunk, out, ensure_ascii=False, separators=(",", ":"))

    file_num = (len(courses_list)-1)//CHUNK_SIZE+1
    with open(os.path.join(output_dir, f"{output_file_prefix}0.min.json"), "w", encoding="utf-8") as out:
        json.dump({"total": file_num}, out,
                  ensure_ascii=False, separators=(",", ":"))
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
    # courses = parse_course(original_data_path)
    with open(original_data_path, "r", encoding="utf-8") as f:
        courses = json.load(f)
    strip_course(courses, output_dir, output_prefix)
    print(f"✔️ 完成處理：{len(courses)} 筆課程資料")


if __name__ == "__main__":
    main()
