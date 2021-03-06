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
curl {{ ingest_agent_url }} --output agent.tar.gz

echo "Moving and extracting Python Clammer agent..."
mv agent.tar.gz /opt/clammer
cd /opt/clammer
tar -xzvf agent.tar.gz

echo "Installing pygtail..."
python3 -m pip install pygtail

echo "Setting permissions on /opt/clammer/..."
chown clammer:clammer /opt/clammer -R

echo "Cleanup..."
mv ./endpoints/agent/* .
rm -r ./endpoints
rm agent.tar.gz -f
