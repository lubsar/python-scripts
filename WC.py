#                                         __
#                                     _.-~  )
#                          _..--~~~~,'   ,-/     _
#                       .-'. . . .'   ,-','    ,' )
#                     ,'. . . _   ,--~,-'__..-'  ,'
#                   ,'. . .  (@)' ---~~~~      ,'
#                  /. . . . '~~             ,-'
#                 /. . . . .             ,-'
#                ; . . . .  - .        ,'
#               : . . . .       _     /
#              . . . . .          `-.:
#             . . . ./  - .          )
#            .  . . |  _____..---.._/ ____ ~ Delfyn ~
#      ~---~~~~----~~~~~~---~~~~----~~~
from collections import Counter


def ui():
    try:
        path = input("Enter path of file to control or type exit to terminate: ")
        file = open(path, mode='r')
        return file
    except FileNotFoundError:
         print('Wrong path !')
         return ui() #TODO, PEP8


def read_file(file):
    lines = file.read()
    words = str.split(lines)
    return words


def word_counter(most_common = 3):
    counter = Counter(read_file(ui()))
    test = counter.most_common(most_common)
    return test


def main():
    print('Word counter')
    print(word_counter())


if __name__ == '__main__':
    main()
