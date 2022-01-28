#!usr/bin/bash
apt update
#apt install -y software-properties-common
#apt install -y build-essential
#apt install -y libssl-dev

#python3.8 installation
#apt install -y python3.8 python3.8-dev
#ln -sf /usr/bin/python3.8 /usr/bin/python3
apt install -y python3-pip
#python3.8 -m pip install --upgrade pip
python3.6 -m pip install --upgrade pip
python3.6 -m pip install -r ./requirements.txt


