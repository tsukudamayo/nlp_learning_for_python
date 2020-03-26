import pandas as pd


def main():
    title_csv = pd.read_csv('sample.csv')
    print(title_csv)
    title = title_csv['タイトル']
    print(title)
    tag_csv = pd.read_csv('kyteatag.csv')
    tag = tag_csv[
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    ]
    print(tag)



if __name__ == '__main__':
    main()
