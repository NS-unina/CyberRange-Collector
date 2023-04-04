import {Schema, model} from "mongoose";

const imageSchema = new Schema({
    timestamp: {
        type: String,
        required: true,
    },
    host: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    }
})

const Image = model('Image', imageSchema)

export default Image;