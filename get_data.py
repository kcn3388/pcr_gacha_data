import argparse
import datetime
import json
import os
import requests
import sys

from typing import Union, List

headers = {
    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-cn"
}


def get_data(url: Union[List[str], str], path: Union[List[str], str]):
    if isinstance(url, list):
        for index in range(len(url)):
            curr_url: str = url[index]
            curr_path: str = path[index]
            print(f"downloading {curr_url}")
            res = requests.get(curr_url, timeout=10, headers=headers).content
            if curr_url.endswith(".json"):
                json_str = json.loads(res.decode("utf-8"))
                with open(curr_path, 'w', encoding='utf-8') as file:
                    json.dump(json_str, file, indent=4, ensure_ascii=False)
            else:
                with open(curr_path, 'wb') as file:
                    file.write(res)

    else:
        print(f"downloading {url}")
        res = requests.get(url, timeout=10, headers=headers).content
        if url.endswith(".json"):
            json_str = json.loads(res.decode("utf-8"))
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(json_str, file, indent=4, ensure_ascii=False)
        else:
            with open(path, 'wb') as file:
                file.write(res)
    now = datetime.datetime.now()
    auto_upload = f"Auto upload in {now}"
    upload = os.path.join(os.path.dirname(__file__), 'auto_upload.md')
    with open(upload, 'w', encoding='utf-8') as file:
        file.write(auto_upload)


parser = argparse.ArgumentParser(description="select which file to download")
parser.add_argument("--every", "-E", action="store_true", help="download all json")
parser.add_argument("--ver", "-V", action="store_true", help="download version json")
parser.add_argument("--unit", "-U", action="store_true", help="download unit_data json")
parser.add_argument("--gacha", "-G", action="store_true", help="download gacha json")

if __name__ == "__main__":
    ver_url = 'https://api.redive.lolikon.icu/gacha/gacha_ver.json'
    gacha_url = 'https://api.redive.lolikon.icu/gacha/default_gacha.json'
    unit_data_url = 'https://api.redive.lolikon.icu/gacha/unitdata.py'

    ver_path = os.path.join(os.path.dirname(__file__), 'gacha_ver.json')
    gacha_path = os.path.join(os.path.dirname(__file__), 'default_gacha.json')
    unit_data_path = os.path.join(os.path.dirname(__file__), 'unitdata.py')

    url_ = [ver_url, gacha_url, unit_data_url]
    path_ = [ver_path, gacha_path, unit_data_path]

    args = vars(parser.parse_args())
    every = args["every"]
    ver = args["ver"]
    unit = args["unit"]
    gacha = args["gacha"]
    if every:
        get_data(url_, path_)
    elif ver:
        get_data(ver_url, ver_path)
    elif unit:
        get_data(unit_data_url, unit_data_path)
    elif gacha:
        get_data(gacha_url, gacha_path)
    else:
        print("not enough args")
