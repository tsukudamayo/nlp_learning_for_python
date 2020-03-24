import re


def ingredient_list_to_dict(strings: str) -> dict:
    _INDENT = -1 # -1, 0, 1
    lines = strings.split('\n')
    print(lines)
    for idx, line in enumerate(lines):
        if line == '':
            del lines[idx]
            continue
        print('line : ', line)
        if line[0] == '　' and _INDENT == -1:
            _INDENT = 0
            del lines[idx - 1]
        elif line[0] == '　' and _INDENT == 0:
            _INDENT = 1
        elif line[0] != '　' and _INDENT == 1:
            _INDENT = -1
        else:
            pass

    print(lines)

    lines = [re.sub('^　', '', w) for w in lines]
    lines = [re.sub('　$', '', w) for w in lines]
    print('sub lines : ', lines)
    lines = [w.split('　') for w in lines]
    print('split lines : ', lines)

    target_dict = {}
    for line in lines:
        if len(line) != 2:
            target_dict.update({line[0]: ''})
            continue
        target_dict.update({line[0]: line[1]})
    print('target_dict :', target_dict)

    return
