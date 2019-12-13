from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk
import re
import math

documentFrequency = {}
documentVector = [0]
forwardIndexTable = {}
backwardIndexTable = {}
termList = []
termTable = {}
postingFileList = []

def forwardIndexing(docPath, docList):
	global forwardIndexTable, termList
	stopWords = set(stopwords.words('english'))
	words_file = open('words', 'w')
	docId = 0

	for fileName in docList:
		# read file text
		f = open(docPath + '/' + fileName.split('.pdf')[0] + '.txt', 'r')
		text = f.read()
		f.close()

		# extract nouns
		tokens = word_tokenize(text)
		tags = nltk.pos_tag(tokens)
		nouns = [tag[0] for tag in tags if tag[1] in ['NN', 'NNP']]

		for noun in nouns:
			# remove stopwords
			if noun in stopWords:
				nouns.remove(noun)

			# set term list, words file and document frequency
			if noun in termList and noun in documentFrequency:
				documentFrequency[noun] += 1
				continue
			termList.append(noun)
			words_file.write(noun + '\n')
			documentFrequency[noun] = 1

		# count frequency of each terms
		term_frequency = Counter(nouns)
		# convert dictionary to list
		term_freq_list = []
		for noun in nouns:
			# set a tuple (term, weight) and append to list
			tup = (noun, term_frequency[noun])
			term_freq_list.append(tup)

		# set forward index table
		docId += 1
		forwardIndexTable[docId] = term_freq_list

	words_file.close()
	print("Indexed forward complete.")

def setDocumentVector(numofDocs):
	global documentFrequency, documentVector, forwardIndexTable, termList
	f = open('documentvector.dat', 'w')

	for docId in range(1, numofDocs + 1):
		vector = {}
		# calculate tf-idf and make document vector sorted by word id
		for termId, term in enumerate(termList):
			idf = math.log2(numofDocs / documentFrequency[term])
			term_freq, totNumofTerm = 0, 0
			for tup in forwardIndexTable[docId]:
				if tup[0] == term: term_freq = tup[1]
				totNumofTerm += tup[1]
			tf = term_freq / totNumofTerm
			tfidf = tf * idf
			if term_freq != 0: vector[term] = (termId + 1, tfidf)
		documentVector.append(vector)
		sorted_vector = sorted(vector.items(), key=lambda x: x[1][0])
		# set a document vector file
		for vec in sorted_vector:
			f.write(str(vec[1][0]) + ':' + str(vec[1][1]) + ' ')
		f.write('\n')

	f.close()
	print("Set document vector complete.")

def backwardIndexing(numofDocs):
	global forwardIndexTable, backwardIndexTable, termList

	for term in termList:
		docIdNfreq_tuple_list = []
		for docId in range(1, numofDocs + 1):
			for tup in forwardIndexTable[docId]:
				if tup[0] == term:
					# set (document id, term frequency)
					inverted_tup = (docId, tup[1])
					docIdNfreq_tuple_list.append(inverted_tup)
		# set backward index table of this term
		backwardIndexTable[term] = docIdNfreq_tuple_list
	print("Indexed backward complete.")

def setInvertedFile():
	global documentVector, backwardIndexTable, termList, termTable, postingFileList
	startLocation = 0

	with open('termtable', 'w') as f:
		for term in termList:
			# set posting file list
			doc_tf_list = backwardIndexTable[term]
			doc_tfidf_list = []
			for tup in doc_tf_list:
				docId = tup[0]
				tfidf = documentVector[docId][term][1]
				doc_tfidf_list.append((docId, tfidf))
			postingFileList += doc_tfidf_list

			# set term table { term : (start location, number of document) }
			numofDoc = len(backwardIndexTable[term])
			termTable[term] = (startLocation, numofDoc)
			startLocation += numofDoc

			# save term table file
			f.write(
				term + ' ' + str(termTable[term][0]) + ' ' + str(termTable[term][1]) + '\n'
			)

	# save inverted file
	with open('postingfile', 'w') as f:
		tuplelist2string = ''
		for elem in postingFileList:
			tuplelist2string += str(elem[0]) + ':' + str(elem[1]) + ' '
		f.write(tuplelist2string)
	print("Set inverted file complete.")


def Indexing(path, docList, numofDocs):
	forwardIndexing(path, docList)
	setDocumentVector(numofDocs)
	backwardIndexing(numofDocs)
	setInvertedFile()
