# Custom Honeypot 

This project is a demonstration on how to set up your own honeypot environmental network that is used to capture incoming SSH connections onto that specific device. Docker is utilized in order to simulate different machines attempting to SSH into the honeypot. Finally, a partial SIEM software (Elasticsearch and Kibana) is used to display the SSH connections onto a GUI.    

# Technologies Used

## Honeypot

- Docker
- Docker Compose 
- Python 

## Monitoring & Visualization

- Elasticsearch
- Kibana 

## Other Tools

- sshfs 

# Prerequisites 

- One Ubuntu device to run partial SIEM and Docker software 
- Another Ubuntu device to be used as the Honeypot   
- Docker installed
- Docker Compose installed 
- Python installed 
- Git installed 

# Setting up the Honeypot 

**NOTE:** Make sure to do these steps on the Honeypot Ubuntu Device. DO NOT PERFORM THESE STEPS ON THE PARTIAL SIEM DEVICE. 

## 1: Update the OS

Run the following commands to update and upgrade the packages

```
sudo apt update && sudo apt upgrade 
``` 

## 2: Clone Cowrie

Cowrie is the honeypot software that we are going to use due to its detailed logs and feedback. Clone the repositroy onto your systme

```
git clone https://github.com/cowrie/cowrie
```

## 3: Install pip and make build

Run these commands to install pip and make build if it isn't in your system yet already

```
sudo apt install python3-pip # Installs pip 
sudo apt install build-essential # Installs make and other useful packages 
```

## 4: Edit the ubuntu sshd_config file 

With your editor (i.e. vi, nano, etc), edit the sshd_config file and uncomment the line where it mentions Port 22 

```
nano /etc/ssh/sshd_config
```

## 5: Configure IP Tables to redirect port 22 to cowrie's port 2222

Run this command

```
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
```

Any SSH connections to port 22 will be treated as an SSH connection going to port 2222 and thus logged by cowrie 

## 6: Modify bashrc to add cowrie's folder to the path

Run the following commands to add cowrie's folder to path

```
nano ~/.bashrc
```

Head to the bottom of the file and add the following paths

```
PATH=/home/ubuntu/.local/bin:$PATH 
PATH=/home/ubuntu/cowrie/bin:$PATH 
```
**NOTE:** Change ubuntu to the name of the current user in session. You can find this name by running the following command

```
whoami
```

Once you are done, save the file and then run the following to re-execute the current commands and configurations within the current session

```
source ~/.bashrc
exec bash 
``` 

## 8: Install python virtual environment inside the cowrie folder 

Cd into the cowrie folder and install python virtual environment within the folder 

```
cd cowrie
python3 -m venv cowrie-env
```

Once the virtual environment is made, activate the virtual environment by running the following

```
source cowrie-env/bin/activate
``` 

## 9: Start Cowrie 

Run cowrie by running the following command:

```
cowrie start
```

To check if cowrie is running, run the following command:

```
cowrie status
```

## 10: Testing Cowrie 

Once cowrie is running, you can visit the __/var/log/cowrie/__ directory to see the log files. These log files will record any SSH attempt into the honeypot. 
If you would like to test if cowrie logs an attacker machine, open a new terminal session and attempt to SSH into the honeypot 

```
ssh root@<honeypot-ip> -p 2222 
``` 

**NOTE:** If you are prompted to enter a password, just press Enter 

# Setting up partial SIEM 

This step focuses on taking the cowrie log file, parsing the log files, inserting them into Elasticsearch, and lastly visualizing the data on Kibana 

**NOTE:** All these steps are done on the machine that is in charge of the partial SIEM system. DO NOT FOLLOW THESE STEPS ON THE HONEYPOT MACHINE  

## 1: Run docker compose inside the cowrie-parser folder 

Cd into the cowrie-parser folder and run the following docker command to install Elasticsearch and Kibana as containers 

```
cd cowrie-parser
docker-compose up -d
``` 

## 2: Use sshfs to mount the cowrie log file onto the current system

SSHFS (SSH File System) is a tool that allows you to mount a remote file system onto your local machine via SSH. In order to mount the log file onto your local machine, run the following command 

```
sshfs <honeypot-username>@<honeypot-ip>:<path-to-log-file-on-remote-system> <local-mount-point>
```

Replace all the fields with the necessary information.

**NOTE:** It is important to note that the best directory for the local-mount-point should be in the __/mnt__ directory. It is also recommended to create a new directory inside of /mnt directory and put the log file within that directory. 

**NOTE:** Another important matter to note is that you should make sure that your log file on the remote system has __read, write, execute__ permissions. This is so that we can successfully use the log file for the parser program. 

## 3: Run parse.py 

Back inside the cowrie-parser folder, run the following

```
python3 parse.py
```

**NOTE:** The values of the log_file_path variable as well as the kibana_url variable (in kibana_post.py) are from environmental variables. Replace them with the necessary values before running the program. 

## 4: Visualizing Data in Kibana 

You can then visit **localhost5601** to see Kibana and set up an index __that has the same name as the one in the kibana_url__ (i.e. http://localhost:9200/log/_doc/ where log is the name of the index)

Once that index is made, you can then visualize the data by creating a dashboard and then selecting how you want your data to be represented (i.e. pie chart, vertical stack, etc)

**NOTE:** Additional data is being sent to the index as this parser is running, so always be sure to refresh your index to see the newly updated data 

## Setting up Attack Simulation 

This step focuses on setting up an attack simulation mechanism such that it will create 10 containers, each with its own ip address, and will attempt to SSH into the honeypot.

**NOTE:** It is recommended do run these steps only after you have your honeypot completeted AND your partial SIEM system completed. 

## 1: Run docker compose inside the attack-simulation folder 

Cd into the attack-simulation folder and run the following docker command to initiate the containers

```
cd attack-simulation
docker-compose up -d 
``` 

## 2: Exec into the containers in order to SSH into a honeypot

With each of the containers running, you can now enter each of the containers and attempt to SSH into the honeypot from within the container. To achieve this, run the following command:

```
docker exec -it <id-of-docker-container> /bin/bash
``` 

Once in the container, you will need to install __openssh-client__ within the container. To do this, run the following command

```
apt-get install -y openssh-client 
```

Once installed, you can now ssh onto your honeypot server by following this format:


```
ssh root@<honeypot-ip> -p 2222
```

Press enter when prompted for the password. 

You can now check the log files to see if the ip address of the container was traced. 

## ALTERNATIVE APPROACH: Router's DMZ

An alternative but risky approach is to log into the router and make it so that __the honeypot is accessible across the entire internet.__ This is done through exposing your honeypot device with the router's DMZ, such that the honeypot device will basically accept external traffic and will thus share the same external IP address as the router. 

You can do all of this by __logging into your router__ depending on your ISP. 
