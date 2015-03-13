
* TO RUN (mac): 
----------------
% mongod &
% python app.py

* TO RUN (ubuntu): 
------------------
% python app.py

*Installation
--------------

1. Update ubuntu:
-----------------

.. code-block:: bash 

		$ sudo apt-get update
		$ sudo apt-get install python-pip

2. Install Mongodb:
-------------------

.. code-block:: bash 

		$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

		$ echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

		$ sudo apt-get update
		$ sudo apt-get install -y mongodb-org


3. Install Python Library:
--------------------------

.. code-block:: bash 

		$ sudo pip install pymongo
		$ sudo pip install flask
		$ sudo apt-get install git

4. A. Install Python lxml module:
---------------------------------

.. code-block:: bash 

		$ sudo apt-get install libxml2-dev libxslt-dev python-dev
		$ sudo pip install pycrypto
		$ sudo apt-get install zlib1g-dev
		$ sudo pip install lxml 

4. B. Build junos-eznc:
-----------------------

.. code-block:: bash 

		$ sudo pip install junos-eznc

5. Install wkhtmltopdf
----------------------

6. %python app.py
------------------

