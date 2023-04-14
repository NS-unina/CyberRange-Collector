import http from 'http';

const createIndexPattern = (req,res,next) => {
    const statusCode = req.dataIfIndexCreated
    if(statusCode == 200){
        const dataToSend = JSON.stringify({
            "attributes": {
              "title": "command*",
              "timeFieldName": "timestamp",
              "fieldFormatMap": "{\"see_more\":{\"id\":\"url\",\"params\":{\"parsedUrl\":{\"origin\":\"http://localhost:5601\",\"pathname\":\"/app/management/opensearch-dashboards/indexPatterns\",\"basePath\":\"\"},\"labelTemplate\":\"Detailed Informations\"}}}"
            }
          })
        const options = {
            method: 'POST',
            hostname: 'opensearch-dashboards',
            port: 5601,
            path: `/api/saved_objects/index-pattern/command`,
            rejectUnauthorized: false,
            headers: {
                'Authorization': 'Basic YWRtaW46YWRtaW4=',
                'Content-Type': 'application/json',
                'osd-xsrf': 'true',
                'securitytenant': 'global'
              }
          };
        
          const proxyReq = http.request(options, (proxyRes) => {
            let data = '';
            proxyRes.on('data', (chunk) => {
              data += chunk;
            });
        
            proxyRes.on('end', () => {
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
    else{
        next()
    }
    
}

export default createIndexPattern