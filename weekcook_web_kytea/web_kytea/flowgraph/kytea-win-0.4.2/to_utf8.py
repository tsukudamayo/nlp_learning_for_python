import sys
import codecs


def main(read_file, output_file):
    fin = codecs.open(read_file, 'r', 'shift_jis')
    fout = codecs.open(output_file, 'w', 'utf-8')
    for row in fin:
        fout.write(row)
    fin.close()
    fout.close()


if __name__ == '__main__':
    read_file = sys.argv[1]
    output_file = sys.argv[2]
    main(read_file, output_file)
