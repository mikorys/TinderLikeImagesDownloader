#Python Standard Library
import json
import shutil
import os

#Python installed Packages
import requests # pip install requests

#  !!!!!!! Paste here X-Auth token below, XauthToken Should be betwen quotes '' for instance 'pasted X-authToken' !!!!!!!!!!
XAuth = 'PASTE X-AUTH TOKEN HERE' 
# !! REMEMBER !!! personal X-AUTH TOKEN changes once a week if script does not work check if it is correct  

# Constants
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOADED_IMAGES_DIRECTORY = DIR_PATH + '/downloadedImages'
TINDER_API_URL = 'https://api.gotinder.com/v2/fast-match/teasers'
HEADERS = {"X-Auth-Token":XAuth}

def createDownloadFolder():
    """Create 
            [if not already exist]
       the directory that images will be downloaded to
    """
    if os.path.isdir(DOWNLOADED_IMAGES_DIRECTORY) == False:
        os.mkdir(DOWNLOADED_IMAGES_DIRECTORY)
        print("Download subFolder successfully created!")

def deleteAllImages():
    """Delete
        all images in the directory that contains the
        downloaded images
    """
    with os.scandir(DOWNLOADED_IMAGES_DIRECTORY) as image_folder:
        for entry in image_folder:
            if entry.is_file():
                os.remove(entry.path)

def download(imageUrl):
    """Download the image url

    Args:
        imageUrl (str): the image url
    """
    try:
        res = requests.get(imageUrl, stream=True)
        filename = str(imageUrl).split("/")[-1]
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(res.raw, out_file)
            shutil.move(DIR_PATH + "/" +filename, DOWNLOADED_IMAGES_DIRECTORY + "/")
        del res
    except:
        pass

def getData():
    """Main function 
    """
    
    createDownloadFolder()
    deleteAllImages()

    #Get content over Tinder
    result = requests.get(TINDER_API_URL, headers=HEADERS)
    response = result.content.decode("utf-8")
    result = json.loads(response.replace("'",'"'))

    # List of users
    users = result.get('data').get('results')


    for user in users:
        #first image of user
        imageUrl= user.get('user').get('photos')[0].get('url')
        download(imageUrl)

if __name__ == "__main__":
    getData()

#TODO Add type checking
#TODO Add parallel download
#TODO Add readme
#TODO download all images of user