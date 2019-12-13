from flask import (
    Blueprint, flash, g, redirect, session, render_template, request, url_for, send_file
)
from werkzeug.exceptions import abort
from werkzeug import secure_filename

from os.path import isfile, join

from index import Indexing
from search import readData, Searching
from ocr import ocr_core
from readDoc import readpdf
from SampleSentence import sample_sentence

import os

bp = Blueprint('page', __name__)
isOCRed, isIndexed = False, False
filepath = '/home/sjw/Documents/Capstone2/pdf list/'
temppath = '/home/sjw/Documents/Capstone2/temp/'

termTable = {}
postingFileList = []
fileNameList = []
docTitleDict = {}
docTxtDict = {}


def getFileList(dirname):
    return [f for f in os.listdir(dirname) if isfile(join(dirname, f))]


@bp.route('/', methods=('GET', 'POST'))
def index():
    """Show main page, to start most tasks at first."""
    global isOCRed, isIndexed, termTable, postingFileList, fileNameList
    fileNameList = getFileList(filepath)

    if isOCRed == False:
        fileNameList = getFileList(filepath)
        for filename in fileNameList:
            title, text = readpdf(filename)
            docTitleDict[filename] = title
            docTxtDict[filename] = text
        db.commit()
        isOCRed = True

    if isIndexed == False:
        # process Indexing
        Indexing('/home/sjw/Documents/Capstone2/temp', fileNameList, len(fileNameList))
        termTable, postingFileList = readData()
        isIndexed = True

    if request.method == 'POST':
        # process Searching
        query = request.form['searchform']
        searchedFileNameList = Searching(query, fileNameList, len(fileNameList), termTable, postingFileList)
        docInfoList = []
        for filename in searchedFileNameList:
            samplesents = sample_sentence(query, docTxtDict[filename])
            docInfoList += [(filename, docTitleDict[filename], samplesents)]
        return render_template('view.html', docInfoList=docInfoList)

    return render_template('index.html')


@bp.route('/view', methods=('GET', 'POST'))
def view():
    global fileNameList

    if request.method == 'POST':
        # process Searching
        query = request.form['searchform']
        searchedFileNameList = Searching(query, fileNameList, len(fileNameList), termTable, postingFileList)
        docInfoList = []
        for filename in searchedFileNameList:
            samplesents = sample_sentence(query, docTxtDict[filename])
            docInfoList += [(filename, docTitleDict[filename], samplesents)]
        return render_template('view.html', docInfoList=docInfoList)


@bp.route('/view/<filename>')
def viewfile(filename):
    try:
        return send_file('/home/sjw/Documents/Capstone2/pdf list/' + filename)
    except Exception as e:
        return str(e)
