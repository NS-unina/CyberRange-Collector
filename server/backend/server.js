import express from 'express';
import morgan from 'morgan';
import imagesRoutes from './routes/imagesRoutes.js'
import connectDB from './utils/db.js';
import cors from 'cors';
import openSearchRoutes from './routes/openSearchRoutes.js'
import {getOSHost, loadEnv} from './utils/env.js'
import { fileURLToPath } from 'url';
import path from 'path'


// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);

// const environment = process.env.NODE_ENV || '';
// const envFilePath = path.resolve(__dirname, `${environment}.env`)
// config({ path: envFilePath });

// Load the environemnt
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
loadEnv(__dirname);



const PORT = process.env.PORT || 9000;

const app = express();

app.use(cors())

app.use(morgan('dev'));

//Routes
app.use('/images', imagesRoutes)
app.use('/openSearch', openSearchRoutes)

app.listen(PORT, () => {
    connectDB().then(() => {
        console.log(`Server running on port: ${PORT}`)
    })
})