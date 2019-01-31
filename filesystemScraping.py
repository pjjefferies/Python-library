# -*- coding: utf-8 -*-
"""
Created on Sat May 14 21:58:01 2016

@author: PaulJ
Derived from "http://stackoverflow.com/questions/12610456/getting-a-file-system-listing-python"
"""

from os import walk as osWalk
#from os import name as osName
from os import stat as OsStat
#from os import startfile as osStartfile
import datetime
import re
from operator import itemgetter
from collections import OrderedDict
from time import time
import locale



def getTree(rootDir, verbose):
    """
    Input:  rootDir: Absolute/Full text path to start directory tree parsing
    
    Output: tree: Dictionary of directory and files found as follows:
                    keys: full path of all directories found
                    values: list of files within 'key' directory
            fileDictLoc: ordered list of filenames and full paths as follows:
                    keys: filenames
                    values: list of lists of full paths where file is found
                            and size of file at this location
    """
    tree = {}
    fileDictLoc = OrderedDict()
    aListOfFiles = []
    for path, dirs, files in osWalk(rootDir):
        tree[path] = []
        for file in files:
            #Save file to dictionary by path
            tree[path].append(file)
            PathWithFile = path + "\\" + file
            #Save file to global list of files
            if len(PathWithFile) < 255:
                fileSize = OsStat(path + "\\" + file).st_size
            else:
                if verbose:
                    print("File Path & Name too long:", PathWithFile + ". Setting file size as 0")
                fileSize = 0            
            aListOfFiles.append([file, path, fileSize])
            if file in fileDictLoc:
                #Found a duplicate filename, add location to list
                tempFileLocs = fileDictLoc[file]
                tempFileLocs.append([path, fileSize])
                fileDictLoc[file] = tempFileLocs
            else:
                #new filename, add path as single element list to O'Dict
                fileDictLoc[file] = [[path, fileSize]]
        tree[path].sort()
        fileDictLoc = OrderedDict(sorted(fileDictLoc.items(), key=lambda t: t[0]))
    return tree, fileDictLoc, aListOfFiles


def print_file_tree(tree):
    # Prepare tree
    dir_list = list(tree.keys())
    dir_list.sort()

    for directory in dir_list:
        print(directory)
        #tree[directory].sort - already done in getTree
        if len(tree[directory]) > 0:
            for f in tree[directory]:
                print("   ", f)
        else:
            print("   Empty of Files")


def save_file_tree(tree, reportFileName, rootDirectoryName):
    treeReport = "Tree File Report for directory: " + rootDirectoryName + "\n\n"
    dir_list = list(tree.keys())
    dir_list.sort()

    for directory in dir_list:
        treeReport += ("\n" + directory + "\n")
        #tree[directory].sort - already done in getTree
        if len(tree[directory]) > 0:
            for f in tree[directory]:
                treeReport += ("   " + f + "\n")
        else:
            treeReport += ("   Empty of Files\n")
    treeReport = treeReport[0:-1]

    treeReport = re.sub('[^A-Za-z0-9 \_\-\.\,\\n\~\$\\\(\)\&\:\#]', '', treeReport)

    try:
        with open(reportFileName, "w") as text_file:
            text_file.write(treeReport)
    except UnicodeEncodeError:
        print("Couldn't save because of UnicodeEncodeError")
        return treeReport
    text_file.close()

    return treeReport


def findDuplicateFiles(fileDictLoc):
    """
    Input:  fileDictLoc: ordered Dict of filename and full paths as follows:
                            keys: filename
                            values: list of directories filename is found in
    Output: dupFileDict: Dictionary of duplicate files found as follows:
                            keys: filename
                            values: list of lists of full paths where file is found
                            and size of file at this location
    """
    dupFileDict = OrderedDict()
    for fileName in fileDictLoc:
        if len(fileDictLoc[fileName]) > 1:
            #Found a duplicate filename
            dupFileDict[fileName] = fileDictLoc[fileName]
    return dupFileDict


def createDuplicateFileReport(duplicateFileList, rootDirectoryName):
    report = "Duplicate File Report for directory: " + rootDirectoryName + "\n\n"
    if len(duplicateFileList) == 0:
        report += "No duplicate files found."
        return report
    for filename in duplicateFileList:
        report += (filename + "\n")
        for fileLocSize in duplicateFileList[filename]:
            report += ("     " + str(locale.format("%d", fileLocSize[1], grouping=True)) + ": " +
                       fileLocSize[0] + "\n")
        report += "\n"
    return report


def createAllFileReport(aListOfFiles, rootDirectoryName):
    report = "All File Report for directory: " + rootDirectoryName + "\n\n"
    if len(aListOfFiles) == 0:
        report += "No files. Get some files. Please come back when you have some files."
        return report
    for filename in aListOfFiles:
        report += (str(locale.format("%d", filename[2], grouping=True)) + ",    " +
                   filename[1] + ", " + filename[0] + "\n")
    return report


if __name__ == '__main__':
    startTime = time()
    #locale.setlocale(locale.LC_ALL, 'en_US')
    aPath = "C:\\Users\\ajeffep\\Documents\\Data"
    #aPath = "C:\\Users\\PaulJ\\Data\\Society and Culture"
    #aPath = "C:\\Users\\PaulJ\\Data"
    #reportSaveLoc = "C:\\Users\\PaulJ\\Data\\Computers & Internet\\Python\\library"
    #aPath = "C:\\Users\\ajeffep\\Documents\\Data\\Honda\\96MY-03MY TRAXXIS"
    reportSaveLoc = "C:\\Users\\ajeffep\\Documents\\Data\\Engineering\\Software\\Library"
    
    datetimeNow = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    treeReportFileName = (reportSaveLoc + "\\Dir_List_Report - " +
                          datetimeNow + ".txt")
    dupFileReportFileName = (reportSaveLoc + "\\Duplicate_File_List_Report - " +
                             datetimeNow + ".txt")
    allFileReportFileName = (reportSaveLoc + "\\All_File_List_Report - " +
                             datetimeNow + ".txt")
    saveTreeReport = True
    saveDuplicateFileReport = True
    saveFileSizeReport = True
    verbose = False

    aTree, aFileDictLoc, aListOfFiles = getTree(aPath, verbose)

    if saveTreeReport:
        #Save Tree Report to File
        treeReport = save_file_tree(aTree, treeReportFileName, aPath)
        #osStartfile(reportFileName)    #acts as double-click in windows - opens report
    
    duplicateFileDict = findDuplicateFiles(aFileDictLoc)
    
    #Sort files by filename
    """
    duplicateFileDict = OrderedDict(sorted(duplicateFileDict.items(),
                                           key=lambda x: x[0]))
    """
    #Sort each duplicate folder listing by each file size
    for aDupFile in duplicateFileDict:
        sortedDirListBySize = sorted(duplicateFileDict[aDupFile],
                                     key=lambda x: -x[1])
        duplicateFileDict[aDupFile] = sortedDirListBySize


    #or Sort files by first (largest) filesize
    duplicateFileDict = OrderedDict(sorted(duplicateFileDict.items(),
                                           key=lambda x: -x[1][0][1]))
    
    
    duplicateFileReport = createDuplicateFileReport(duplicateFileDict, aPath)
    duplicateFileReport = re.sub('[^A-Za-z0-9 \_\-\.\,\\n\~\$\\\(\)\&\:\#]', '', duplicateFileReport)
    
    if saveDuplicateFileReport:
        with open(dupFileReportFileName, "w") as text_file:
            text_file.write(duplicateFileReport)
        text_file.close()
    
    #Sort aListOfFiles
    aListOfFiles = sorted(aListOfFiles, key=lambda x: -x[2])
    allFileReport = createAllFileReport(aListOfFiles, aPath)
    allFileReport = re.sub('[^A-Za-z0-9 \_\-\.\,\\n\~\$\\\(\)\&\:\#]', '', allFileReport)
    
    if saveFileSizeReport:
        with open(allFileReportFileName, "w") as text_file:
            text_file.write(allFileReport)
        text_file.close()
    
    
    totalTime = time() - startTime
    print("Time for report: {:4.1f} seconds.".format(totalTime))
    print("Vebose:", verbose)