try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import shutil
from pdf2text import extText
from convpdf2img import convert_pdf
from title_extraction import title_extraction

filepath = '/home/sjw/Documents/Capstone2/pdf list/'
temppath = '/home/sjw/Documents/Capstone2/temp/'

def readpdf(filename):
    imgpath = temppath + filename.split('.pdf')[0]
    text = extText(filepath, filename)
    convert_pdf(filepath + filename, imgpath)
    title_extraction(imgpath)

    f = open(temppath + filename.split('.pdf')[0] + '.txt', 'w')
    title = pytesseract.image_to_string(Image.open(imgpath + '/title.png'), lang='eng')
    f.write(text)
    f.close()

    shutil.rmtree(imgpath)
    return title, text
