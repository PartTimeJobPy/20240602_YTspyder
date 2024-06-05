# -*- coding:UTF-8 -*-
import re, requests, time, random, json
from requests.models import Response
from typing import Union, List, Any, Dict, Mapping, Callable


def parse_m3u8_text(m3u8_text):
    m3u8_text = m3u8_text.split()
    encode_info = [line for line in m3u8_text if line.startswith('#EXT-X-KEY:')][0]
    pattern = r"#EXT-X-KEY:METHOD=(.*),URI=\"(.*)\""

    ## 获得加密method 和 key.key的url
    match = re.search(pattern, encode_info)
    if match:
        method = match.group(1)
        key_url = match.group(2)
    else:
        raise '解析失败'

    ## 获得ts文件url
    ts_list = [line for line in m3u8_text if '.ts?' in line]
    return method, key_url, ts_list

def merge_ts_to_mp4(filename, ts_file_list):
    with open(filename, mode='ab') as f1:
        for ts_file in ts_file_list:
            with open(ts_file, mode='rb') as f2:
                f1.write(f2.read())