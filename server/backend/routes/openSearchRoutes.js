import {Router} from 'express';
import { postBulk, getCSV } from './handlers/openSearchHandlers.js';
import checkIndexExists from '../middleware/checkIndexExists.js';
import createIndex from '../middleware/createIndex.js';
import createIndexPattern from '../middleware/createIndexPattern.js';
import bodyParser from 'body-parser';

import passport from 'passport';
import { registerStrategy } from '../config/passport-config.js'

const router = Router();

registerStrategy()

router.post('/bulk', 
    passport.authenticate('bearer', { session: false }),
    checkIndexExists, 
    createIndex,
    createIndexPattern, 
    bodyParser.json(), 
    postBulk)

router.get('/:host', getCSV)

export default router;