import time

import nesearch as ne


def main():
    read_file = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_4_1/detail_103522_proc4_1.txt'
    food_list, tag_list, prob_list = ne.text_to_list(read_file)
    print('food_list')
    print(food_list)
    print('tag_list')
    print(tag_list)
    print('prob_list')
    print(prob_list)
    for f, t, p in zip(food_list, tag_list, prob_list):
        time.sleep(1)
        print(f)
        print(t)
        print(p)


if __name__ == '__main__':
    main()
