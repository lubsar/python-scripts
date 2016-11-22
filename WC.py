import os


def request_input():
    path = input("Enter path of file to control or type exit to terminate: ")
    if path == 'exit':
        exit(0)

    file = None

    try:
        file = open(path, mode='r')
    except FileNotFoundError:
        print('Wrong path !')
        request_input()

    if os.path.isfile(path):
        return file
    else:
        print('{} is not a file'.format(path))
        request_input()


def main():
    print('Word counter')
    file = request_input()

    data = {}
    lines = file.readlines()

    for line in lines:
        line = line.strip('\n')
        if line == '':
            continue
        line_words = line.split(' ')
        for word in line_words:
            if word == ' ':
                continue
            if word in data.keys():
                data[word] += 1
            else:
                data[word] = 1

    for k,v in data.items():
        print(k, v)

    print()
    request_input()


if __name__ == '__main__':
    main()