import { fileURLToPath } from 'url';
import { dirname } from 'path';
import path from 'path';
import fs from 'fs';
import Image from '../../models/Image.js';


const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function splitFileName(fileName) {
    const regex = /^(.*?)_(\d{4}-\d{2}-\d{2}-\d{2}:\d{2}:\d{2})\.(\w+)$/;
    const match = fileName.match(regex);
    if (match) {
      const name = match[1];
      const [year, month, day, hour, minute, second] = match[2].split(/[-: ]/);
      const date = Date.UTC(year, month-1, day, hour, minute, second);
      const timestamp = new Date(date);
      return [name, timestamp];
    }
    return [];
  }
  
const createImage = async (req,res) => {
    const files = req.files
    const {host} = req.params
    if(!host){
        return res.status(400).json('Host not found')
    }
    Object.keys(files).forEach(async key => {
        const filepath = path.join(__dirname, '/../uploads', host, files[key].name)
        const [name, timestamp] = splitFileName(files[key].name);
        const image = new Image({ timestamp: `${timestamp}`, host: `${host}`, title: `${files[key].name}`})
        await image.save()
        files[key].mv(filepath, (err) => {
            if (err) return res.status(500).json({status: "error", message: err})
        })
    })

    return res.json({status: 'success'})
}

const getGif = async (req,res) => {
    try{
        const {host} = req.params
        if(!host){
            return res.status(404).json('Host not found')
        }
        res.sendFile(path.join(__dirname, `/../uploads/${host}/${host}.gif`))
    } catch(error){
        console.log(error);
    }
}

const getSingleImage = async (req,res) => {
    try{
        const {id} = req.params
        if(!id){
            return res.status(404).json('Id not found')
        }
        const image = await Image.findById(id).exec()
        res.sendFile(path.join(__dirname, `/../uploads/${image.host}/${image.title}`))
    } catch(error){
        console.log(error)
    }
}

const getImagesName = async (req,res) => {
    try{
        const {host} = req.params
        if(!host){
            return res.status(404).json('Host not found')
        }
        const regex = new RegExp('\\.(png|jpeg)(?!.*\\.(png|jpeg))$');
        const images = await Image.find({host: host, title: regex}).exec()
        return res.json(images)
    } catch (error){
        console.log(error)
    }
}

const deleteImages = async (req,res) => {
    try{
        const {host} = req.params
        if(!host){
            return res.status(404).json('Host not found')
        }
        await Image.deleteMany({ host: host });
        
        const folder = path.join(__dirname, `/../uploads/${host}`)

        fs.rm(folder, { recursive: true }, err => {
        if (err) {
            return res.json({message: `${host} not found!`})
        }

        return res.json({message: `${host} is deleted!`})
        })
    } catch(error){
        console.log(error)
    }
}

const getFolderNames = async (req,res) => {
    try{
        const folder = path.join(__dirname, `/../uploads`)
        fs.readdir(folder, { withFileTypes: true }, (err, files) => {
            if (err) {
              res.status(500).json({status:'error', message: 'Internal error'})
            }
            const directories = files.filter(file => file.isDirectory()).map(file => file.name);
            res.json(directories)
        });
    } catch (error) {
        console.log(error)
    }
}

export {createImage, getGif, getImagesName, deleteImages, getSingleImage, getFolderNames}