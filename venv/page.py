from flask import (
    Blueprint, flash, g, redirect, session, render_template, request, url_for, send_file
)
from werkzeug.exceptions import abort
from werkzeug import secure_filename

from venv.auth import login_required
from venv.db import get_db

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
#fileNameListInDB = []
fileNameList = []
docTitleDict = {}
docTxtDict = {}


def getFileList(dirname):
    return [f for f in os.listdir(dirname) if isfile(join(dirname, f))]


@bp.route('/', methods=('GET', 'POST'))
def index():
    """Show main page, to start most tasks at first."""
    global isOCRed, isIndexed, termTable, postingFileList, fileNameList#, fileNameListInDB
    db = get_db()
    fileNameList = getFileList(filepath)

    if isOCRed == False:
        fileNameList = getFileList(filepath)
        #fileNameListInDB = db.execute('SELECT filename FROM document ORDER BY id',).fetchall()
        for filename in fileNameList:
            #if filename not in fileNameListInDB:
                #convert_pdf(filepath + filename, temppath + filename.split('.pdf')[0])
                #title_extraction(temppath, filename.split('.pdf')[0])
                #title = ocr_core(filename)
                title, text = readpdf(filename)
                docTitleDict[filename] = title
                docTxtDict[filename] = text
                #db.execute('INSERT INTO document (filename, title, text) VALUES (?, ?, ?)', (filename, title, text))
        db.commit()
        isOCRed = True

    if isIndexed == False:
        # process Indexing
        #fileNameListInDB = db.execute('SELECT filename FROM document ORDER BY id',).fetchall()
        Indexing('/home/sjw/Documents/Capstone2/temp', fileNameList, len(fileNameList))
        termTable, postingFileList = readData()
        isIndexed = True

    if request.method == 'POST':
        # process Searching
        query = request.form['searchform']
        searchedFileNameList = Searching(query, fileNameList, len(fileNameList), termTable, postingFileList)
        docInfoList = []
        for filename in searchedFileNameList:
            #docInfoList += db.execute('SELECT * FROM document WHERE filename = ?', (filename))
            samplesents = sample_sentence(query, docTxtDict[filename])
            docInfoList += [(filename, docTitleDict[filename], samplesents)]
        return render_template('view.html', docInfoList=docInfoList)

    return render_template('index.html')


@bp.route('/view', methods=('GET', 'POST'))
def view():
    global fileNameList
    db = get_db()

    if request.method == 'POST':
        # process Searching
        query = request.form['searchform']
        searchedFileNameList = Searching(query, fileNameList, len(fileNameList), termTable, postingFileList)
        docInfoList = []
        for filename in searchedFileNameList:
            #docInfoList += db.execute('SELECT * FROM document WHERE filename = ?', (filename))
            samplesents = sample_sentence(query, docTxtDict[filename])
            docInfoList += [(filename, docTitleDict[filename], samplesents)]
        return render_template('view.html', docInfoList=docInfoList)

    #return redirect(url_for('page.index'))


@bp.route('/view/<filename>')
def viewfile(filename):
    try:
        return send_file('/home/sjw/Documents/Capstone2/pdf list/' + filename)
    except Exception as e:
        return str(e)

"""
@bp.route('/upload', methods=('POST'))
def upload():
    return render_template('upload.html')


@bp.route('/uploadprocess', methods=('GET', 'POST'))
def uploadProcess():
    db = get_db()
    if request.method == 'POST':
        f = request.files['file']
        f.save('/home/sjw/Documents/Capstone2/pdf list/' + secure_filename(f.filename))

        title = ocr_core(f.filename)

        db.execute('INSERT INTO document (filename, title) VALUES (?, ?)',
            (f.filename, title))
        db.commit()
        return redirect(url_for('page.index'))

    return render_template('index.html')
"""
