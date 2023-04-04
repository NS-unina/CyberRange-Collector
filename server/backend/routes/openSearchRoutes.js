import {Router} from 'express';
import { postBulk, getCSV } from './handlers/openSearchHandlers.js';
import bodyParser from 'body-parser';

import passport from 'passport';
import { registerStrategy } from '../config/passport-config.js'

const router = Router();

registerStrategy()

router.post('/bulk', passport.authenticate('bearer', { session: false }), bodyParser.json(), postBulk)
router.get('/:host', getCSV)

export default router;