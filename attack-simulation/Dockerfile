FROM ubuntu:latest

# Install certain features to the attacker machines 
RUN apt-get update && apt-get install -y openssh-client sshpass

# Create attack script that attempts to SSH into the honeypot 
RUN echo '#!/bin/bash\n\
while true; do\n\
  sshpass -p "" ssh -o StrictHostKeyChecking=no -p 2222 root@${HONEYPOT_IP}\n\
  sleep $(( RANDOM % 60 + 30 ))\n\
done' > /attack.sh && chmod +x /attack.sh

# Run the bash script 
CMD ["/attack.sh"]