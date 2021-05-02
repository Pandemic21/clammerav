#!/bin/bash

which python3 &>/dev/null
if [ $? -eq 0 ]
then
  # python3 is installed
  echo "Python3 is installed, continuing..."
else
  echo "Python3 not installed, installing..."
  apt-get install python3
fi

echo "Making Clammer user..."
useradd --system --no-create-home clammer

echo "Making /opt/clammer/..."
mkdir /opt/clammer

echo "Downloading Clammer agent..."
curl http://127.0.0.1:8000/endpoints/ingest/6fbc21b0-2b38-45a7-80c2-0cb3753ac2e8/agent.tar.gz --output agent.tar.gz

echo "Moving and extracting Python Clammer agent..."
mv agent.tar.gz /opt/clammer
cd /opt/clammer
tar -xzvf agent.tar.gz

echo "Installing pygtail..."
python3 -m pip install pygtail

echo "Installing requests..."
python3 -m pip install requests

echo "Creating join URL..."
echo http://127.0.0.1:8000/endpoints/ingest/6fbc21b0-2b38-45a7-80c2-0cb3753ac2e8/join/ >> ingest_join_url

echo "Setting permissions on /opt/clammer/..."
chown clammer:clammer /opt/clammer -R

echo "Cleanup..."
mv ./endpoints/agent/* .
rm -r ./endpoints
rm agent.tar.gz -f

echo "Running clammer_init.py..."
python3 clammer_init.py
