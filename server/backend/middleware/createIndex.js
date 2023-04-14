import https from 'https';

const createIndex = (req,res,next) => {
    const statusCode = req.dataIfIndexExists
    if(statusCode == 200){
        next()
    }
    else{
        const dataToSend = JSON.stringify({
            "settings": {
              "index": {
                "number_of_shards": 2,
                "number_of_replicas": 1
              }
            },
            "mappings": {
              "properties": {
                "host_id": {
                  "type": "text"
                },
                "session_id": {
                  "type": "text"
                },
                "working_directory": {
                  "type": "text"
                },
                "timestamp": {
                  "type": "date",
                  "format": "strict_date_time"
                },
                "command": {
                  "type": "text"
                },
                "output": {
                  "type": "text"
                },
                "see_more": {
                  "type": "text"
                }
              }
            }
          })
        const options = {
            method: 'PUT',
            hostname: 'opensearch-node1',
            port: 9200,
            path: `/command`,
            rejectUnauthorized: false,
            headers: {
                'Authorization': 'Basic YWRtaW46YWRtaW4=',
                'Content-Type': 'application/json'
              }
          };
        
          const proxyReq = https.request(options, (proxyRes) => {
            let data = '';
            proxyRes.on('data', (chunk) => {
              data += chunk;
            });
        
            proxyRes.on('end', () => {
                req.dataIfIndexCreated = proxyRes.statusCode
              next()
            });
          });
        
          proxyReq.on('error', (error) => {
            console.error(error);
            res.status(500).json({ error: 'Internal server error' }); 
          });
        
          proxyReq.write(dataToSend);
          proxyReq.end();
    }
    
}

export default createIndex