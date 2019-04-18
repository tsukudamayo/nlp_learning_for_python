def main():
    sentence = "a boy ate sushi with hands"
    words = sentence.split(' ')    
    length = len(words)
    cell = [[''] * length for i in range(length)]
    print(cell)

    print(words)
    for l in range(1, len(words)+1):
        for i in range(0, len(words) - l):
            j = i + l
            print(j)
            for k in range(i+1, j-1):
                print('i', i)
                print('j', j)
                print('k', k)


if __name__ == '__main__':
    main()















