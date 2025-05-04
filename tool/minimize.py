import json


def minimize_json(input_file, output_file):
    """
    Minimize a JSON file by removing whitespace and formatting.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output minimized JSON file.
    """
    with open(input_file, 'r', encoding="utf-8") as f:
        data = json.load(f)

    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(data, f, separators=(',', ':'))


if __name__ == "__main__":
    import os
    import sys

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python minimize.py <input_file> <output_file>")
        sys.exit(1)
    input_file = args[0]
    output_file = args[1]
    if not os.path.isfile(input_file):
        print(f"Error: {input_file} does not exist.")
        sys.exit(1)

    minimize_json(input_file, output_file)
    print(f"✅ 完成: {input_file} -> {output_file}")
