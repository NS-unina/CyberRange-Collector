import React, { useState, useEffect } from "react";
import "./App.css";

const apiUrl = process.env.API_URL || 'http://localhost';
const apiPort = process.env.API_PORT || 9000;

function App() {
  const [data, setData] = useState("");
  const [names, setNames] = useState([""]);
  const [image, setImage] = useState("");

  const [host, setHost] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const param_time = params.get('timestamp');
    const param_host = params.get('host');
    setHost(params.get('host'));
    getData(param_host, param_time)
  },[] );
  
  const getData = (n_host, time) => {
    fetch(`${apiUrl}:${apiPort}/images/gif/${n_host}`)
      .then((res) => res.blob())
      .then((data) => setData(URL.createObjectURL(data)))
      .catch((err) => console.log(err))

    fetch(`${apiUrl}:${apiPort}/images/names/${n_host}`)
      .then((res) => res.json())
      .then((data) => filterOnTimestamp(data,time))
      .then((filteredName) => setNames(filteredName))
      .catch((err) => console.log(err))
  }

  const filterOnTimestamp = (array,time) => {

    return array.filter((obj) => {
      const objDate = new Date(obj.timestamp).getTime();
      const filterTimestamp = new Date(time).getTime();
      return objDate >= filterTimestamp;
    })
    .sort((a, b) => {
      const timestampA = new Date(a.timestamp).getTime();
      const timestampB = new Date(b.timestamp).getTime();
      return timestampA - timestampB;
    });
  }

  function handleClick(id) {
    fetch(`${apiUrl}:${apiPort}/images/single/${id}`)
      .then(response => response.blob())
      .then(item => setImage(URL.createObjectURL(item)))
      .catch((err) => console.log(err))
  }

  function convertToCSV(jsonData) {
    let csv = '';
    const keys = [];

    jsonData.forEach(item => {
        Object.keys(item).forEach(key => {
            if (!keys.includes(key)) {
                keys.push(key);
            }
            if (typeof item[key] === 'object' && item[key] !== null) {
                Object.keys(item[key]).forEach(nestedKey => {
                    if (!keys.includes(`${key}.${nestedKey}`)) {
                        keys.push(`${key}.${nestedKey}`);
                    }
                });
            }
        });
    });

    csv += keys.join(',') + '\n';

    jsonData.forEach(item => {
        const row = [];
        keys.forEach(key => {
            let value = item;
            key.split('.').forEach(k => value = value[k]);
            row.push(value);
        });
        csv += row.join(',') + '\n';
    });

    return csv;
}

  function downloadCSV(){
    fetch(`${apiUrl}:${apiPort}/openSearch/${host}`)
      .then((res) => res.json())
      .then((data) => {
        let hits_data = [];
        for (let index = 0; index < data.hits.hits.length; index++) {
          hits_data.push(data.hits.hits[index]);
        }
        console.log(hits_data)
        const csvData = convertToCSV(hits_data);
        console.log(csvData)
        const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
        const csv_url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", csv_url);
        link.setAttribute("download", "data.csv");
        document.body.appendChild(link);
        link.click();
      })      
      .catch((err) => console.log(err))
      
  }

  return (
    <div className="App">
      <img src={data} alt="Gif" />
      <button onClick={() => downloadCSV()}>Download</button>
      <table>
      <thead>
        <tr>
          <th>Host</th>
          <th>Titolo</th>
          <th>Azioni</th>
        </tr>
      </thead>
      <tbody>
        {names.map((item, index) => (
          <tr key={index}>
            <td>{item.host}</td>
            <td>{item.title}</td>
            <td>
              <button onClick={() => handleClick(item._id)}>Dettagli</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    <img src={image} alt="Single Screenshot" />
    </div>
  );
}


export default App;
