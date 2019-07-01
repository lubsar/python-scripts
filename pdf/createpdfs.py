import os
import sys
import getopt
import shutil
from fpdf import FPDF

from PIL import Image

#create PDF file from images in source directory
def create_PDF_file(sourcedir, dest, name):
    print('Creating {}/{}'.format(dest, name))

    pdf = FPDF(orientation="P",unit="mm",format="A4")
    pdf.set_compression(True)
    pdf.add_page()
    pdf.add_font('FreeMono', '', 'font/FreeMono.ttf', uni=True)
    pdf.set_margins(0,0,0)

    files = os.listdir(sourcedir)

    # create destination directory if not present
    if not os.path.exists(dest):
        os.makedirs(dest)

    # write index
    if 'index.txt' in files:
        print('Index found')
        pdf.set_font('FreeMono',size=12)

        with open('{}/index.txt'.format(sourcedir),'r', encoding='cp1250') as index:
            entries = index.readlines()

            for entry in entries:
                pagenum = int(entry[-4:])
                link = pdf.add_link()
                pdf.set_link(link, page=pagenum +1)
                pdf.set_x(0)
                # print('{} {}'.format(entry[:-6],pagenum))

                pdf.write(5, '{}...........{}\n'.format(entry[:-6],pagenum), link)

    print('Index built')

    # remove all except .jpg
    files = list(filter(lambda x: x.endswith('.jpg'), files))

    # sort by numbers
    files.sort(key=lambda x: int(x[-8:-4]))

    print('Adding {} images'.format(len(files)))

    for imag in files:
        pdf.image(name='{}/{}'.format(sourcedir, imag), type='JPG', w=210, h=297)

    print('Writing pdf file...')

    pdf.output('{}/{}'.format(dest, name), 'F')
    pdf.close()

    print('Done\n')


# scale images in directory
def scale_images(sourcedir, dst, factor):
    files = os.listdir(sourcedir)

    # remove all except .jpg
    files = list(filter(lambda x: x.endswith('.jpg'), files))

    startProgress('Scaling {} pages'.format(len(files)))

    counter = 1
    for file in files:
        # print('Scaling {} {}/{}'.format(file, counter, len(files)))
        progress(counter/len(files)*100)

        img = Image.open('{}/{}'.format(sourcedir, file))
        width, height = img.size

        width = int(width * factor)
        heigh = int(height * factor)

        img.thumbnail((width, height), Image.ANTIALIAS)
        img.save('{}/{}'.format(dst, file),'JPEG')

        counter += 1

    endProgress()
    print('')


# create pdf
def create_pdf(source, dest, workdir, scale):
    # create working directory if not present
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    # scale images
    scale_images(source, workdir, scale)

    #copy index file
    files = os.listdir(source)
    if 'index.txt' in files:
        shutil.copy2('{}/{}'.format(source, 'index.txt'), '{}/{}'.format(workdir, 'index.txt'))

    # create pdf file
    create_PDF_file(workdir, dest, 'output.pdf');


# create pdfs recursively
def create_pdfs_recursive(source, dest, workdir, scale):
    files = os.listdir(source)

    createdPDF = False

    for file in files:
        if os.path.isdir('{}/{}'.format(source, file)):
            print('Found directory {}'.format(file))
            create_pdfs_recursive('{}/{}'.format(source, file), '{}/{}'.format(dest, file), '{}/{}'.format(workdir, file), scale)
        if file.startswith('IMG') and not createdPDF:
            print('{} contains images, creating PDF'.format(source))
            create_pdf(source, dest, workdir, scale)
            createdPDF = True


def cleanup(workdir):
    print('Deleting work directory {}'.format(workdir))
    shutil.rmtree(workdir)
    print('Done')

def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()


def main(argv):
    if(len(argv) < 2):
        print('createdpdfs.py <source directory> <destination directory> --scale <scale> --work <work directory>')
        sys.exit(0)

    source = argv[0]
    destination = argv[1]
    workdirectory = 'workdir'
    scalingfactor = 1.0

    try:
          opts, args = getopt.getopt(argv[2:],'',['scale=','work='])
    except getopt.GetoptError:
          print('createdpdfs.py <source directory> <destination directory> --scale <scale> --work <work directory>')
          sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('createdpdfs.py <source directory> <destination directory> --scale <scale> --work <work directory>')
            sys.exit()
        elif opt in ('--scale'):
            scalingfactor = arg
        elif opt in ('--work'):
              workdirectory = arg

    create_pdfs_recursive(source, destination, workdirectory, scalingfactor)

if __name__ == "__main__":
  main(sys.argv[1:])
