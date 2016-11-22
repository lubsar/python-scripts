import os

def uajko():
    path = input("Enter path of file to control or type exit to terminate: ")
    if path == 'exit':
        exit(0)

    file = None

    try:
        file = open(path, mode='r')
    except FileNotFoundError:
        print('Wrong path !')
        uajko()

    if os.path.isfile(path):
        return file
    else:
        print('{} is not a file'.format(path))
        uajko()
        
def main():
   print('Word counter')
   file = uajko()

   data = {}

   lines = file.readlines()
   for line in lines:
        if line == '':
            continue
        line = line.strip('\n')
        riadok = line.split(' ')
        for slovo in riadok:
            if slovo == ' ':
                continue
            if slovo in data.keys():
                data[slovo] = data[slovo] + 1
            else:
                data[slovo] = 1

   for k,v in data.items():
        print(k,v);

   print()
   uajko()

if __name__ == '__main__':
    main()