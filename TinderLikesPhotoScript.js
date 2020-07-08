/////////////////////////////////// Created by Reddit user N4styCartpet/ wykop.pl user mikorys
const Axios = require('axios')
const Fs = require('fs')
const Path = require('path')
const FsExtra = require('fs-extra')

// !!!!!!!!!! Paste here X-Auth token below, XauthToken Should be betwen quotes '' for instance 'pasted X-authToken' !!!!!!!!!!
let XAuth = 'PASTE X-AUTHTOHKEN HERE' 
// !! REMEMBER !!! personal X-AUTH TOKEN changes once a week if script does not work check if it is correct  

const directory = __dirname + '/downloadedImages'
const tinderApiURL = 'https://api.gotinder.com/v2/fast-match/teasers'
let config = {
    headers: {
        'X-Auth-Token': `${XAuth}`
    }
}

function createDownloadFolder() {//if no subDirectory exists create one
    if (!Fs.existsSync(directory)){
        Fs.mkdirSync(directory);
        console.log("Download subFolder successfully created!")
    }

}

async function deleteAllImages() {//remove all images from driectory - using FS-Extra module
    try {
        await FsExtra.emptyDir(directory)
        console.log('Folder successfully cleared')
    } catch (err) {
        console.log('Clearing Folder Error')
        console.error(err)
    }
}

async function download(url, photoNo) {//main function download 10 last like images
    const path = Path.resolve(__dirname, 'downloadedImages', `TinderImageNo ${photoNo}.jpeg`)

    const response = await Axios({
        method: 'GET',
        url: url,
        responseType: 'stream'
    })

    response.data.pipe(Fs.createWriteStream(path))

    return new Promise((resolve, reject) => {
        response.data.on('end', () => {
            console.log(`Tinder Photo No ${photoNo} successfully`)
            resolve()
        })
        response.data.on('error', err => {
            reject(err)
        })
    })
}


 function getData() {
    createDownloadFolder()
    deleteAllImages()
    Axios.get(tinderApiURL, config)
        .then(response => {
            var count = Object.keys(response.data.data.results).length
            var imageUrl= ''
            for (let i=0; i<count;i++){
                imageUrl= response.data.data.results[i].user.photos[0].url
                download(imageUrl,i+1)
            }
        })
        .catch(err => console.log(err, err.response))

}

getData()
