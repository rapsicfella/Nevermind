#!usr/bin/bash
apt update
apt install -y software-properties-common
apt install -y build-essential gcc wget
apt install -y libssl-dev git


#Cmake 3.20.2 Installation
wget https://github.com/Kitware/CMake/releases/download/v3.21.3/cmake-3.21.3.tar.gz
tar -zxvf cmake-3.21.3.tar.gz
rm cmake-3.21.3.tar.gz
cd cmake-3.21.3
./bootstrap
make -j3
make install

cd ..
rm -rf cmake-3.21.3

#Python 3.8 and pip3 installation
apt install -y python3.8 python3.8-dev
ln -sf /usr/bin/python3.8 /usr/bin/python3
apt install -y python3-pip
python3.8 -m pip install --upgrade pip


#OpenDDS C++ installtion
wget https://download.objectcomputing.com/OpenDDS/OpenDDS-3.18.1.tar.gz
tar -xvf OpenDDS-3.18.1.tar.gz
rm OpenDDS-3.18.1.tar.gz
mv OpenDDS-3.18.1 OpenDDS
cd OpenDDS && ./configure && make -j3

cd ..

#pyopendds installation
git clone https://github.com/oci-labs/pyopendds.git
source ./OpenDDS/setenv.sh
cd pyopendds
pip3 install .

cd ..

#Paho C MQTT installation
git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
git checkout v1.3.8
cmake -Bbuild -H. -DPAHO_ENABLE_TESTING=OFF -DPAHO_BUILD_STATIC=ON \
    -DPAHO_WITH_SSL=ON -DPAHO_HIGH_PERFORMANCE=ON
cmake --build build/ --target install
ldconfig

cd ..

#Paho C++ MQTT installation
git clone https://github.com/eclipse/paho.mqtt.cpp
cd paho.mqtt.cpp
cmake -Bbuild -H. -DPAHO_BUILD_STATIC=ON \
    -DPAHO_BUILD_DOCUMENTATION=FALSE -DPAHO_BUILD_SAMPLES=FALSE
cmake --build build/ --target install
ldconfig

cd ..

rm -rf paho.mqtt.c paho.mqtt.cpp

