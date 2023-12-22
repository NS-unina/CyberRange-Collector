import {Router} from 'express';
import fileUpload from 'express-fileupload';
import fileExtLimiter from '../middleware/fileExtLimiter.js';
import filesPayloadExists from '../middleware/filesPayloadExists.js';
import {createImage, getGif, getImagesName, deleteImages, getSingleImage, getFolderNames} from './handlers/imageHandlers.js';
import passport from 'passport';
import { registerStrategy } from '../utils/passport-config.js'


const router = Router();

registerStrategy()

//GET Routes
router.get('/gif/:host', getGif)

router.get('/names/:host', getImagesName)

router.get('/single/:id', getSingleImage)

router.get('/folders', getFolderNames)

//POST Routes
router.post('/upload/:host',
    passport.authenticate('bearer', { session: false }),
    fileUpload({ createParentPath: true}),
    filesPayloadExists,
    fileExtLimiter(['.png','.jpg','.jpeg','.gif']),
    createImage
)

//DELETE Routes
router.delete('/delete/:host', passport.authenticate('bearer', { session: false }), deleteImages)

export default router;