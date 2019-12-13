import linecache
import math
import nltk
from nltk.tokenize import word_tokenize

def readTermTableFile():
	termTable = {}
	with open('termtable', 'r') as f:
		data = f.read().split('\n')
		for line in data:
			if line == '': break
			record = line.split()
			# term : (start location, number of document)
			termTable[record[0]] = (int(record[1]), int(record[2]))
	print('Read term table file complete.')
	return termTable


def readPostingFile():
	postingFileList = []
	with open('postingfile', 'r') as f:
		data = f.read().split(' ')
		for fv in data:
			if fv == '': break
			docId = int(fv.split(':')[0])
			tfidf = float(fv.split(':')[1])
			postingFileList += [(docId, tfidf)]
	print('Read posting file complete.')
	return postingFileList


def readDocumentVector(docId):
	vectorOfDoc = {}
	stringOfVector = linecache.getline('documentvector.dat', docId).split('\n')[0]
	stringOfElements = stringOfVector.split(' ')
	for strofElem in stringOfElements:
		if strofElem == '': break
		termId = int(strofElem.split(':')[0])
		tfidf = float(strofElem.split(':')[1])
		vectorOfDoc[termId] = tfidf
	return vectorOfDoc


def analyzeQuery(query, numofDocs, termTable):
	#global termTable
	#dupQterms = query.split(' ')
	tokens = word_tokenize(query)
	tags = nltk.pos_tag(tokens)
	nounsDupQterms = [tag[0] for tag in tags if tag[1] in ['NN', 'NNP']]
	qterms = list(set(nounsDupQterms))
	qtermCount, qtermWeight, totNumofqTerm = {}, {}, len(nounsDupQterms)

	for qterm in nounsDupQterms:
		if qterm not in qtermCount: qtermCount[qterm] = 1
		else: qtermCount[qterm] += 1

	for qterm in qterms:
		qtf, idf = 0, 0
		if qterm in termTable:
			doc_freq = termTable[qterm][1]
			idf = math.log2(numofDocs / doc_freq)
			qtf = qtermCount[qterm] / totNumofqTerm
		qtfidf = (0.5 + 0.5 * qtf) * idf
		qtermWeight[qterm] = qtfidf

	return qterms, qtermWeight


def calcSimilarity(qterms, qtermWeight, termTable, postingFileList):
	#global termTable, postingFileList
	docList = []
	similarityOfDoc = {}

	# check term of query which document it has
	for qterm in qterms:
		if qterm not in list(termTable.keys()):
			qterms.remove(qterm)
			continue
		(startLoc, numofDoc) = termTable[qterm]
		for docInfo in postingFileList[startLoc:startLoc+numofDoc+1]:
			docId = docInfo[0]
			if docId not in docList:
				docList.append(docId)

	# read document vector and calculate cosine similarity
	for docId in docList:
		vectorOfDoc = readDocumentVector(docId)
		termIdList = list(vectorOfDoc.keys())
		sumofWeightSqrOfDoc, sumofWeightOfDocXQuery, sumofWeightSqrOfQuery = 0, 0, 0
		for termId in termIdList:
			weightOfDoc = vectorOfDoc[termId]
			sumofWeightSqrOfDoc += weightOfDoc * weightOfDoc
			with open('words', 'r') as f:
				lines = f.readlines()
			term = lines[termId-1].split('\n')[0]
			if term in qterms:
				sumofWeightOfDocXQuery += weightOfDoc * qtermWeight[term]
		for qterm in qterms:
			sumofWeightSqrOfQuery += qtermWeight[qterm] * qtermWeight[qterm]
		similarity = sumofWeightOfDocXQuery /\
					(math.sqrt(sumofWeightSqrOfDoc) * math.sqrt(sumofWeightSqrOfQuery))
		similarityOfDoc[docId] = similarity

	sortedSimOfDocList = sorted(similarityOfDoc.items(), key=lambda x: x[1], reverse=True)
	return sortedSimOfDocList


def searchDocuments(qterms, qtermWeight, docNameList, termTable, postingFileList):
	sortedSearchDocNameList = []
	sortedSimOfDocList = calcSimilarity(qterms, qtermWeight, termTable, postingFileList)
	for docInfo in sortedSimOfDocList:
		docId = docInfo[0]
		sortedSearchDocNameList.append(docNameList[docId-1])

	"""
	# print searched document
	for i in range(20):
		docId, weight = sortedSimOfDocList[i]
		ithResult = str(i) + '. ' + docNameList[docId-1]\
		 			+ ' (docId: ' + str(docId) + ', weight: ' + str(weight) + ')'
		print(ithResult)
	"""
	return sortedSearchDocNameList


def readData():
	termTable = readTermTableFile()
	postingFileList = readPostingFile()
	return termTable, postingFileList


def Searching(query, docNameList, numofDocs, termTable, postingFileList):
	qterms, qtermWeight = analyzeQuery(query, numofDocs, termTable)
	searchedDocList = searchDocuments(qterms, qtermWeight, docNameList, termTable, postingFileList)
	return searchedDocList
