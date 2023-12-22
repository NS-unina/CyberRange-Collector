import https from 'https';
import { getOSHost, getOSUser, getOSPassword} from './env.js';
import { Client }  from '@opensearch-project/opensearch';

const CRC_COMMAND_MAPPING = {
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
                }
            }
  }

const CRC_SCREEN_MAPPING = {
    "properties": {
      "image": {
        "type": "binary"
      },
      "win_name": {
        "type": "text"
      },
      "host_id": {
        "type": "text"
      }
    }
}

const findMapping = (indexName) => {
  if (indexName == 'crc-screenshot') {
    return CRC_SCREEN_MAPPING;
  } else if (indexName == 'crc-command') {
    return CRC_COMMAND_MAPPING;

  }
}


const indexExists = async (indexName) => {
  const client = new Client({
    node: `https://${getOSHost()}:9200`,
    auth: {
      username: getOSUser(),
      password: getOSPassword()
    },
    ssl: {
    // ca: fs.readFileSync('./http_ca.crt'),
    rejectUnauthorized: false
  }});
    const exists = await client.indices.exists({ index: indexName });
    return exists;
}
// Create the index only if it doesn't exist
const createIndex = async function (indexName) {
  const client = new Client({
    node: `https://${getOSHost()}:9200`,
    auth: {
      username: getOSUser(),
      password: getOSPassword()
    },
    ssl: {
    // ca: fs.readFileSync('./http_ca.crt'),
    rejectUnauthorized: false
    }, 
    headers: {
    'Content-Type': 'application/json'
  }

  });
  const exists = await indexExists(indexName);
  const mapping = findMapping(indexName);

  if (!exists) {
    const response = await client.indices.create({
      index: indexName,
      body: {
        mapping
      }
    });

      console.log(response);
  } else {
    console.log(`Index '${indexName}' already exists.`);
  }
}
const createDocument = async function (indexName, document) {
  const client = new Client({
    node: `https://${getOSHost()}:9200`,
    auth: {
      username: getOSUser(),
      password: getOSPassword()
    },
    ssl: {
    // ca: fs.readFileSync('./http_ca.crt'),
    rejectUnauthorized: false
    }, 
    headers: {
    'Content-Type': 'application/json'
  }

  });
  await client.index({
    index: indexName,
    body: document,
    refresh: true
  })
}



const sendOpensearchReq = (req, res, method, path, sendData, callback = () => {}) => {
  if (sendData) {
    var dataToSend = ""
    req.body.map ((data) => {
      dataToSend += `${JSON.stringify(data)}\n`
    })

  }
  const options = {
    method,
    hostname: getOSHost(),
    port: 9200,
    path,
    rejectUnauthorized: false,
    headers: {
        'Authorization': `Basic ${getCreds()}`,
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
      callback(data, proxyRes.statusCode);
    //   const jsonData = JSON.parse(data);
    //   res.json(jsonData); 
    });
  });

  proxyReq.on('error', (error) => {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  });

  if (sendData) {
    proxyReq.write(dataToSend);
  }
  proxyReq.end();


}

// Create a document in the index

export {sendOpensearchReq,  indexExists, createIndex, createDocument};

