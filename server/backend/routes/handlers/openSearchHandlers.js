import https from 'https';

const postBulk = (req,res) => {
  var dataToSend = ""
  req.body.map ((data) => {
    dataToSend += `${JSON.stringify(data)}\n`
  })
  const options = {
    method: 'POST',
    hostname: 'opensearch-node1',
    port: 9200,
    path: '/_bulk',
    rejectUnauthorized: false,
    headers: {
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Content-Type': 'application/json'
      }
  };
  const proxyReq = https.request(options, (proxyRes) => {
    console.log(`statusCode: ${proxyRes.statusCode}`);
    let data = '';
    proxyRes.on('data', (chunk) => {
      data += chunk;
    });

    proxyRes.on('end', () => {
      const jsonData = JSON.parse(data);
      res.json(jsonData); 
    });
  });

  proxyReq.on('error', (error) => {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  });

  proxyReq.write(dataToSend);
  proxyReq.end();


}

const getCSV = (req,res) => {
  const {host} = req.params;
  const options = {
    method: 'GET',
    hostname: 'opensearch-node1',
    port: 9200,
    path: `/command/_search?q=host_id:${host}`,
    rejectUnauthorized: false,
    headers: {
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Content-Type': 'application/json'
      }
  };

  const proxyReq = https.request(options, (proxyRes) => {
    console.log(`statusCode: ${proxyRes.statusCode}`);
    let data = '';
    proxyRes.on('data', (chunk) => {
      data += chunk;
    });

    proxyRes.on('end', () => {
      const jsonData = JSON.parse(data);
      res.json(jsonData); 
    });
  });

  proxyReq.on('error', (error) => {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' }); 
  });

  proxyReq.end();

}

const checkIndex = (req,res) => {
  
}

export {postBulk, getCSV, checkIndex}