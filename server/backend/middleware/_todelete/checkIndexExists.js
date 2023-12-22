import sendOpensearchReq from '../../utils/opensearchAPI.js';

const checkIndexExists = (req, res, next) => {
    const {index} = req.params
    console.log("In check index exists");
    console.log(index);

    sendOpensearchReq(req, res, 'HEAD', `/${index}`, false, (data, statusCode) => {
          req.dataIfIndexExists = statusCode
          console.log(req.dataIfIndexExists)
          next()
    });

}

export default checkIndexExists;