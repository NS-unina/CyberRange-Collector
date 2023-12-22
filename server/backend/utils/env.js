import path from 'path'
import {config} from 'dotenv';

const loadEnv = (dirname) => {
    const environment = process.env.NODE_ENV || '';
    const envFilePath = path.resolve(dirname, `${environment}.env`)
    config({ path: envFilePath });
}

const getOSHost = () => process.env.OS_HOST
const getOSUser = () => process.env.OS_USER
const getOSPassword = () => process.env.OS_PWD

const getCreds = () => Buffer.from(`${getOSUser()}:${getOSPassword()}`, 'utf8').toString('base64')  


export {loadEnv, getOSHost, getOSUser, getOSPassword, getCreds};