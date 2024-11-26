# Custom Honeypot 

This project is a demonstration on how to set up your own honeypot environmental network that is used to capture incoming SSH connections onto that specific device. Docker is utilized in order to simulate different machines attempting to SSH into the honeypot. Finally, a SIEM software (Elasticsearch and Kibana) is used to display the SSH connections onto a GUI.    

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

- One Ubuntu device to run SIEM and Docker software 
- Another Ubuntu device to be used as the Honeypot   
- Docker installed
- Docker Compose installed 
- Python installed 
- Git installed 

# Setting up the Honeypot 

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

# Setting up SIEM 

## 1: TO BE ADDED 