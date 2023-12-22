import https from 'https';
import {sendOpensearchReq, createIndex as createOSIndex, indexExists, createDocument} from '../../utils/opensearchAPI.js';

const postBulk = (req,res) => {
  sendOpensearchReq(req, res, 'POST', '/_bulk', true, (data, statusCode) => {
      const jsonData = JSON.parse(data);
      res.json(jsonData); 
  });
}


const createIndex = async (req, res) => {
    console.log("IN create req");
    const index = req.params.index
    const document = req.body.document
    try {
      // await createIndex(indexName)
      await createOSIndex(index);
      await createDocument(index, document);
      res.json("NOT IMPLEMENTED")
    }
     catch (error) {
      console.log(error)
      res.status(503).json("Some error")
    }


  }
  // var dataToSend = ""
  // req.body.map ((data) => {
  //   dataToSend += `${JSON.stringify(data)}\n`
  // })
  // const options = {
  //   method: 'POST',
  //   hostname: getOSHost(),
  //   port: 9200,
  //   path: '/_bulk',
  //   rejectUnauthorized: false,
  //   headers: {
  //       'Authorization': `Basic ${getCreds()}`,
  //       'Content-Type': 'application/json'
  //     }
  // };
  // const proxyReq = https.request(options, (proxyRes) => {
  //   console.log(`statusCode: ${proxyRes.statusCode}`);
  //   let data = '';
  //   proxyRes.on('data', (chunk) => {
  //     data += chunk;
  //   });

  //   proxyRes.on('end', () => {
  //     const jsonData = JSON.parse(data);
  //     res.json(jsonData); 
  //   });
  // });

  // proxyReq.on('error', (error) => {
  //   console.error(error);
  //   res.status(500).json({ error: 'Internal server error' });
  // });

  // proxyReq.write(dataToSend);
  // proxyReq.end();


const getCSV = (req, res) => {
  const {host} = req.params;
  const path = `/command/_search?q=host_id:${host}`;

  _sendOpensearchReq(req, res, 'GET', path, false, (data, statusCode) => {
      const jsonData = JSON.parse(data);
      res.json(jsonData); 
  });

  // const options = {
  //   method: 'GET',
  //   hostname: getOSHost(),
  //   port: 9200,
  //   path: `/command/_search?q=host_id:${host}`,
  //   rejectUnauthorized: false,
  //   headers: {
  //       'Authorization': `Basic ${getCreds()}`,
  //       'Content-Type': 'application/json'
  //     }
  // };

  // const proxyReq = https.request(options, (proxyRes) => {
  //   console.log(`statusCode: ${proxyRes.statusCode}`);
  //   let data = '';
  //   proxyRes.on('data', (chunk) => {
  //     data += chunk;
  //   });

  //   proxyRes.on('end', () => {
  //     const jsonData = JSON.parse(data);
  //     res.json(jsonData); 
  //   });
  // });

  // proxyReq.on('error', (error) => {
  //   console.error(error);
  //   res.status(500).json({ error: 'Internal server error' }); 
  // });

  // proxyReq.end();

}


export {postBulk, getCSV, createIndex}