# Update
sudo apt-get update
sudo apt-get install -y python-pip

#Install Mongodb:
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

sudo apt-get update
sudo apt-get install -y mongodb-org

# Install Python Library:
sudo pip install pymongo
sudo pip install flask
sudo apt-get install -y  git

# Install Python lxml module:
sudo apt-get install -y libxml2-dev libxslt-dev python-dev
sudo pip install pycrypto
sudo apt-get install zlib1g-dev
sudo pip install lxml 

# Build junos-eznc:
sudo pip install junos-eznc
sudo pip install pymongo