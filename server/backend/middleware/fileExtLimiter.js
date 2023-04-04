import path from "path"

const fileExtLimiter = (allowedExtArray) => {
    return (req,res,next) => {
        const files = req.files

        Object.keys(files).forEach(key => {
            const regex = '\\.(png|jpeg|jpg|gif)(?!.*\\.(png|jpeg|jpg|gif))$';
            const match = files[key].name.match(regex);
            if(!match){
                delete req.files[key]
            }
            
        })
        next()
    }
}

export default fileExtLimiter