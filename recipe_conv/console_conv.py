class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'


_INGREDIENT = ['アボカド', '塩鮭', '生クリーム', 'チーズ（ピザ用）', '塩', 'ブラックペッパー']


def main():
    # print(Color.GREEN + 'Green' + Color.END)
    # print(Color.RED + 'RED' + Color.RED)

    sample_file = 'weekcook/ner_result/sample_ner_result.txt'

    f = open(sample_file, 'r', encoding='utf-8')
    lines = f.read()
    f.close()
    # print('lines : ', lines)
    split_lines = lines.split(' ')
    # print('split_lines : ', split_lines)

    # ---------
    # color
    # ---------
    for line in split_lines:
        if line.find('F') >= 0:
            print(Color.RED + line + Color.END, end='')
        elif line.find('T') >= 0:
            print(Color.CYAN + line + Color.END, end='')
        elif line.find('Sf') >= 0:
            print(Color.GREEN + line + Color.END, end='')
        elif line.find('D') >= 0:
            print(Color.GREEN + line + Color.END, end='')
        elif line.find('焼') >= 0 and line.find('Ac') >= 0:
            print(Color.YELLOW + line + Color.END, end='')
        elif line.find('。') >= 0:
            print(line)
        else:
            print(line, end='')

    # ------------------
    # convert param tag
    # ------------------
    param_to_word = {}
    word_to_param = {}
    parameters = {}
    count = 1
    for line in split_lines:
        param_num = 'param' + str(count)
        # print('param_num')
        # print(param_num)
        line = line.replace('=', '')
        if line.find('F') >= 0:
            target = line.split('/')[0]
            if target in _INGREDIENT:
                if target not in word_to_param:
                    param_to_word.update({param_num: target})
                    word_to_param.update({target: param_num})
                    parameters.setdefault(param_num, {})
                    parameters[param_num].setdefault('val', target)
                    parameters[param_num].setdefault('type', 'ingredient')
                    count += 1
                else:
                    param_num = word_to_param[target]
                line = '<' + param_num + '>'
            else:
                pass
            print(Color.RED + line + Color.END, end='')

        elif line.find('T') >= 0 and line.find('cm') < 0:

            target = line.split('/')[0]
            if target.find('火') < 0:
                if target not in word_to_param:
                    param_to_word.update({param_num: target})
                    word_to_param.update({target: param_num})
                    parameters.setdefault(param_num, {})
                    parameters[param_num].setdefault('val', target)
                    parameters[param_num].setdefault('type', 'tool')
                    count += 1
                else:
                    param_num = word_to_param[target]

                line = '<' + param_num + '>'

            else:
                pass

            print(Color.CYAN + line + Color.END, end='')

        elif line.find('cm') >= 0:

            target = line.split('/')[0]
            if target not in word_to_param:
                param_to_word.update({param_num: target})
                word_to_param.update({target: param_num})
                parameters.setdefault(param_num, {})
                parameters[param_num].setdefault('val', target)
                parameters[param_num].setdefault('type', 'unit')
                count += 1
            else:
                param_num = word_to_param[target]

            line = '<' + param_num + '>'
            print(Color.GREEN + line + Color.END, end='')

        elif line.find('Sf') >= 0:

            target = line.split('/')[0]
            if target.isdigit() == True:
                if target not in word_to_param:
                    param_to_word.update({param_num: target})
                    word_to_param.update({target: param_num})
                    parameters.setdefault(param_num, {})
                    parameters[param_num].setdefault('val', target)
                    parameters[param_num].setdefault('type', 'quantity')
                    count += 1
                else:
                    param_num = word_to_param[target]

                line = '<' + param_num + '>'
                print(Color.GREEN + line + Color.END, end='')
            else:
                print(line, end='')

        elif line.find('D') >= 0:

            target_num = line.split('/')[0]
            target_min = int(float(target_num) * 0.7)
            target_max = int(target_num)
            target_list = [target_min, target_max]
            for target in target_list:
                param_num = 'param' + str(count)
                if target not in word_to_param:
                    param_to_word.update({param_num: target})
                    word_to_param.update({target: param_num})
                    parameters.setdefault(param_num, {})
                    parameters[param_num].setdefault('val', target)
                    parameters[param_num].setdefault('type', 'quantity')
                    count += 1
                else:
                    param_num = word_to_param[target]

                line = '<' + param_num + '>'
                print(Color.GREEN + line + Color.END, end='')

        elif line.find('焼') >= 0 and line.find('Ac') >= 0:

            target = line.split('/')[0]
            # if target not in word_to_param:
            #     param_to_word.update({param_num: target})
            #     word_to_param.update({target: param_num})
            # else:
            #     param_num = word_to_param[target]
            # line = '<' + param_num + '>'

            print(Color.YELLOW + line + Color.END, end='')

            count += 1

        elif line.find('。') >= 0:
            print(line)
        else:
            print(line, end='')

    # print('param_to_word', param_to_word)
    # print('word_to_param', word_to_param)
    print('################ word to param ################')
    for k, v in param_to_word.items():
        print(k, v)
    # for k, v in word_to_param.items():
    #     print(k, v)

    print('################ parameters ################')
    for k, v in parameters.items():
        print(k, v)


if __name__ == '__main__':
    main()
