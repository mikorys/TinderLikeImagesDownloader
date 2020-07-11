from flask import Flask, render_template
import os
from os import listdir
from os.path import isfile, join
from pprint import pprint as print
import sys

image_folder = './downloadedImages'

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder=image_folder)

def get_image_filename_in_the_download_folder():
    onlyfiles = ['downloadedImages/'+f for f in listdir(image_folder) if isfile(join(image_folder, f))]
    return onlyfiles

@app.route('/')
def home():
    images = get_image_filename_in_the_download_folder()
    return render_template('index.html', images=images)

if __name__ == "__main__":
    app.run(debug=True)