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
