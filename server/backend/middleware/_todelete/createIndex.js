import https from 'https';
// import { getOSHost, getCreds} from '../utils/env.js';

const createIndex = (req, res, next) => {
    const statusCode = req.dataIfIndexExists
    const {index, schema} = req.params
    if(statusCode == 200){
        next()
    } else {
        console.log("TO IMPLEMENT")
        next();
    }
}

export default createIndex;