import os
import argparse
import pandas as pd

from crawl.cofopdl import fetch_courses
from hook.analysis import course_format_df
from tool.strip import strip_course_df


def save_courses(year: int, term: int, output_dir: str) -> None:
    """
    抓取課程資料並儲存為 TSV 檔案
    :param year: 民國學年度，如 113
    :param term: 學期：1 、 2 或 3
    """
    courses = fetch_courses(year, term)
    if not courses:
        print("沒有抓到任何課程資料")
        return

    # 格式化課程資料
    courses_df = course_format_df(pd.DataFrame(courses))

    # 移除所有 \t
    courses_df = courses_df.map(
        lambda x: x.replace("\t", "") if isinstance(x, str) else x)

    # 儲存為 TSV 檔案
    strip_course_df(courses_df, output_dir)
    print(f"課程資料已儲存至 {output_dir}，"
          f"共 {len(courses_df)} 筆課程資料")


def main():
    parser = argparse.ArgumentParser(description="抓取並儲存課程資料")
    parser.add_argument("-y", "--year", type=int, required=True,
                        help="民國學年度，如 113")
    parser.add_argument("-t", "--term", type=int, required=True,
                        help="學期：1 、 2 或 3")
    parser.add_argument("-o", "--out", type=str,
                        help="輸出目錄，預設為 ../frontend/public/data/{year}-{term}")
    args = parser.parse_args()

    if not args.out:
        args.out = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "..", "frontend", "public", "data",
            f"{args.year}-{args.term}"))

    save_courses(args.year, args.term, args.out)


if __name__ == "__main__":
    main()
