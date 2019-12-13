import slate3k as slate

def extText(path, filename):
    f = open(path + filename, 'rb')
    print(filename)
    extracted_total_text = slate.PDF(f)
    repl_extracted_text = ""
    for extracted_pageof_text in extracted_total_text:
        repl_extracted_text += extracted_pageof_text.replace('-\n', '')\
                                                    .replace('\n', ' ')\
                                                    .replace('\x0c', ' ')
    return repl_extracted_text

#filepath = '/home/sjw/Documents/Capstone2/pdf list/'
#filename = 'Oliveira_Fast_CNN-Based_Document_ICCV_2017_paper.pdf'
#text = extText(filepath, filename)
#sentences = [sentence + '.' for sentence in text.split('.') if 'layout' in sentence]
#print(sentences[0] + ' ... ' + sentences[1] + ' ...')
