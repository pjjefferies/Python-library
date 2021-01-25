# -*- coding: utf-8 -*-.
"""
Created on Sun Jan 26 22:10:20 2020

@author: PaulJ
"""

# Here are all the installs and imports you will need for your word cloud
#  script and uploader widget

# !pip install wordcloud
# !pip install fileupload
# !pip install ipywidgets
# !jupyter nbextension install --py --user fileupload
# !jupyter nbextension enable --py fileupload

import wordcloud
# import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
import fileupload
import io
# import sys

# This is the uploader widget


def _upload():

    _upload_widget = fileupload.FileUploadWidget()

    def _cb(change):
        global file_contents
        decoded = io.StringIO(change['owner'].data.decode('utf-8'))
        filename = change['owner'].filename
        print('Uploaded `{}` ({:.2f} kB)'.format(
            filename, len(decoded.read()) / 2 ** 10))
        file_contents = decoded.getvalue()

    _upload_widget.observe(_cb, names='data')
    display(_upload_widget)


_upload()

f = open("C:/Users/PaulJ/Data/News & Media/Books/t8.shakespeare.txt", "r")
# f = open("C:\\Users\\PaulJ\\Data\\Education\\Online Courses\\Coursera Data "
#          + "Science Capstone\\en_US.twitter.txt", "r")
file_contents = f.read()


def calculate_frequencies(file_contents):
    """
    # Here is a list of punctuations and uninteresting words you can use to.

    # process your text
    """
    # punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    punctuations = "!()-[]{};:'" + r'"\,<>./?@#$%^&*_~'
    punctuations = set(punctuations)
    uninteresting_words = [
        "the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i",
        "me", "my", "we", "our", "ours", "you", "your", "yours", "he", "she",
        "him", "his", "her", "hers", "its", "they", "them", "their", "what",
        "which", "who", "whom", "this", "that", "am", "are", "was", "were",
        "be", "been", "being", "have", "has", "had", "do", "does", "did",
        "but", "at", "by", "with", "from", "here", "when", "where", "how",
        "all", "any", "both", "each", "few", "more", "some", "such", "no",
        "nor", "too", "very", "can", "will", "just"]

    # LEARNER CODE START HERE
    # for char in punctuations:
    #     file_contents = file_contents.replace(char, "")
    file_contents = ''.join(c for c in file_contents if c not in punctuations)

    word_dict = {}
    file_contents_list = file_contents.lower().split()
    for word in file_contents_list:
        if word in uninteresting_words:
            continue
        if word not in word_dict:
            word_dict[word] = 0
        word_dict[word] = word_dict[word] + 1

    # wordcloud
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(word_dict)
    return cloud.to_array()


# Display your wordcloud image

myimage = calculate_frequencies(file_contents)
plt.imshow(myimage, interpolation='nearest')
plt.axis('off')
plt.show()
