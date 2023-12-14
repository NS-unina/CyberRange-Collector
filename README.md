# CyberRange-Collector
This tool stores the input and output of all commands executed from each terminal session of the virtual machine. It also collects screenshots taken each  second and it produces a JSON file as output which contains all those informations. After the JSON file is produced, the tool sends this informations to a web proxy which stores the screenshots and displays the data using OpenSearch Dashboards.

## Getting Started
### Prerequisites
First of all you have to install the dependencies so go into the project directory and type:
```shell
pip install -r requirements.txt
```

You need to have: 
* Scrot (sudo apt-get install -y scrot)
* Script
* Python
* xdotool
* bc

In order to run the server:
* docker
* docker-compose

On kali distro: 
```
sudo apt install -y docker.io docker-compose

# If you want your user to let use docker
sudo usermod -aG docker $USER
sudo systemctl enable docker --now
```

### Starting Server
To start the server that will store the data, you have to go to the server directory inside the project directory and type:
```shell
cd server
docker-compose up
```
---
**NOTE**
Before run the server, increase the `vm.map.size` parameter: 
```
sysctl -w vm.max_map_count=262144
```
You can put permanently by adding 
```
vm.max_map_count=262144
```
in the `/etc/sysctl.conf` file.
---



The compose will start three services:
* Opensearch instance
* Backend instance
* Client instance

### Start Logging
To start logging you need to open a terminal session in the folder where the file *log_tool.sh* is and type
```shell
source log_tool.sh -start
```
From now on, all terminal sessions will be logged and screenshots will be taken every 1 second. 

If you want to log terminal sessions with another screenshot rate you have to type:
```shell
source log_tool.sh -start -rate 10
```
From now on, all terminal sessions will be logged and screenshots will be taken with a rate of 10 screenshots/second.

If you don't want to take screenshots you have to type:
```shell
source log_tool.sh -start -noscreen
```
The help option is given if you type:
```shell
source log_tool.sh -help
```
### Stop Logging
When you type
```shell
source log_tool.sh -stop
```
The tool stops logging and starts to elaborate the stored informations.
It takes all the logs stored in the `/tmp/log-collector` folder and generate JSON file which contains an entry for all terminal session started, with command input, output, working directory and timestamp, like this:

```JSON
{"host": 
{"session_name": 
[{"working_directory": "...",
"timestamp": "...",
"command": "...", 
"output": "..."}, 
{"working_directory": "...",
...}]}
}
```
You can find this JSON file at this path: `/../CyberRange-Collector/logs/`.

### Upload data 
To upload data run: 
```
source log_tool.sh -upload
```

It will upload data in the server. Data can be visualized by the OpenSearch Dashboard. 

The forma of generated indexes is as follows: 
- `command`

### Data Visualization
At this point, you can reach OpenSearch Dashboards where you will find all the session logs collected. Each command has a link to the web app which shows a gif representative of the session captured. Inside the web app, you can also download a .csv file containing all the informations.

### Authors
* Marco Longobardi
* Manuele Toscano
* Gaetano Perrone

