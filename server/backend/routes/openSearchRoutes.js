import {Router} from 'express';
import { postBulk, getCSV, createIndex } from './handlers/openSearchHandlers.js';
import bulkCheckIndexExists from '../middleware/bulkCheckIndexExists.js';
import bulkCreateIndex from '../middleware/bulkCreateIndex.js';
import bulkCreateIndexPattern from '../middleware/bulkCreateIndexPattern.js';




import bodyParser from 'body-parser';

import passport from 'passport';
import { registerStrategy } from '../utils/passport-config.js'

const router = Router();

registerStrategy()

router.post('/bulk', 
    passport.authenticate('bearer', { session: false }),
    bulkCheckIndexExists, 
    bulkCreateIndex,
    bulkCreateIndexPattern, 
    bodyParser.json(), 
    postBulk)

router.get('/:host', getCSV)

router.put('/:index', 
    passport.authenticate('bearer', { session: false }),
    bodyParser.json({limit: '50mb'}), 
    createIndex,
)

    // bodyParser.json(), 
    // postBulk)

export default router;