import os
import json

_ACTION_CATEGORY_FILE = '../recipe_level/action_category/orangepage/action_category.json'
_DST_DIR = './action_time/orangepage'
_DST_FILE = 'action_category.json'

_PARAMS_SPEC = {
    "加熱": 2,
    "混ぜる": 1,
    "おく": 1,
    "切る": 1
}


def main():
    if os.path.exists(_DST_DIR) is False:
        os.makedirs(_DST_DIR)

    with open(_ACTION_CATEGORY_FILE, 'r', encoding='utf-8') as r:
        jsondata = json.load(r)
    print(jsondata)
    keys = jsondata.keys()
    print(keys)
    outputdata = {}
    for k in keys:
        print(jsondata[k])
        key = jsondata[k]
        outputdata[k] = _PARAMS_SPEC[key]
    print(outputdata)
    dst_file_path = os.path.join(_DST_DIR, _DST_FILE)
    with open(dst_file_path, 'w', encoding='utf-8') as w:
        json.dump(outputdata, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
