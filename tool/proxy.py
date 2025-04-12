import os
import subprocess


def run_mitmproxy():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../hook/save.py"))
    cmd = [
        "mitmdump",
        "-s", script_path,
        "--set", "flow_detail=0"
    ]
    return subprocess.Popen(cmd)
