import https from 'https';
import { getOSHost } from '../utils/env.js';


const bulkCheckIndexExists = (req, res, next) => {
    
    const options = {
        method: 'HEAD',
        hostname: getOSHost(),
        port: 9200,
        path: `/command`,
        rejectUnauthorized: false,
        headers: {
            'Authorization': `Basic ${getCreds()}`,
            'Content-Type': 'application/json'
          }
      };
    
      const proxyReq = https.request(options, (proxyRes) => {
        let data = '';
        proxyRes.on('data', (chunk) => {
          data += chunk;
        });
    
        proxyRes.on('end', () => {
          req.dataIfIndexExists = proxyRes.statusCode
          next()
        });
      });
    
      proxyReq.on('error', (error) => {
        console.error(error);
        res.status(500).json({ error: 'Internal server error' }); 
      });
      proxyReq.end();
    
}

export default bulkCheckIndexExists