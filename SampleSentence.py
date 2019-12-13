import nltk
from nltk.tokenize import word_tokenize

def sample_sentence(query, text):
    tokens = word_tokenize(query)
    tags = nltk.pos_tag(tokens)
    nounsDupQterms = [tag[0] for tag in tags if tag[1] in ['NN', 'NNP', 'NNG']]
    qterms = list(set(nounsDupQterms))

    sentences ,result, i = [], '', 0
    for qterm in qterms:
        if i == 2: break
        for sentence in text.split('.'):
            if qterm in sentence:
                if (sentence + '.') not in sentences:
                    sentences.append(sentence + '.')
                    i += 1
                    break
    
    for i in range(len(sentences)):
        if i > 0: result += ' ... '
        if i == 2: break
        result += sentences[i]

    return result
