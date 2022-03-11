# -*- coding: utf-8 -*-

import json, re
import pandas as pd


def find_value(html, key, num_chars=2, separator='"'):
    """ Find matched string in html page.
    """
    if html.find(key) == -1:
        return ''
    else:
        pos_begin = html.find(key) + len(key) + num_chars
        pos_end = html.find(separator, pos_begin)
        return html[pos_begin: pos_end]


def find_json(json_str, key):
    """ Find a valid json object based on key in the string.
    """
    if json_str.find(key) == -1:
        return {}
    else:
        pos_end = pos_begin = json_str.find(key) + len(key)
        num_bracket = 1
        for pos_idx in range(pos_begin, len(json_str)):
            if json_str[pos_idx] == '{':
                num_bracket += 1
            elif json_str[pos_idx] == '}':
                num_bracket -= 1
                if num_bracket == 0:
                    pos_end = pos_idx
                    break
        return fix_json(json_str[pos_begin - 1: pos_end + 1])


def search_dict(partial, key):
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                yield v
            else:
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list):
        for i in partial:
            for o in search_dict(i, key):
                yield o


def fix_json(json_str):
    """ Fix the json string because python json module cannot handle double quotes well.
    """
    while True:
        try:
            json_obj = json.loads(json_str)
            break
        except Exception as e:
            unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
            while unexp >= 1:
                if json_str[unexp - 1] == '"':
                    json_str = json_str[: unexp - 1] + json_str[unexp:]
                    break
                unexp -= 1
    return json_obj


def append_df(df, existing_file_name, index):
    try:
        existing_df = pd.read_csv(existing_file_name)
    except pd.errors.EmptyDataError:
        existing_df = pd.DataFrame()
    # Non-overlapping columns are filled with NaN values
    final_df = pd.concat([existing_df, df])
    final_df.to_csv(existing_file_name, index=index)

