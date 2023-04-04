import express from 'express';
import morgan from 'morgan';
import imagesRoutes from './routes/imagesRoutes.js'
import connectDB from './config/db.js';
import cors from 'cors';
import openSearchRoutes from './routes/openSearchRoutes.js'
import {config} from 'dotenv';
config();

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