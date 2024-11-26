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

# Setting up SIEM 

## 1: TO BE ADDED 