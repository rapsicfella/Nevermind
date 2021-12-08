#! /bin/bash

trap "trap_ctrlc" 2

function trap_ctrlc ()
{
    # perform cleanup here
    echo "Ctrl-C caught...performing clean up"
 
    echo "Doing cleanup"
 
    # exit shell script with error code 2
    # if omitted, shell script will continue execution
    docker stop VideoStreamingContainer OTAContainer
    kill -9 $(ps -ef | grep " python" | awk '{print $2}')
    mv nohup.out nohup.out.$(date +%s)
    exit 2
}

#trap "trap_ctrlc" 2



docker run -d --rm --net=host --name VideoStreamingContainer wipro-vs:latest

docker run -d --rm --net=host -v /home/nvidia/HVAC_VS_OD_OTA_v1.7/:/home/HVAC_VS_OD_OTA_v1.7/ --name OTAContainer wipro-ota:latest
CUR_DIR=`realpath .`
echo $CUR_DIR
UI_DIR="/home/nvidia/HVAC_VS_OD_OTA_v1.7/nativeUI"
SCRIPTS_DIR="/home/nvidia/HVAC_VS_OD_OTA_v1.7/OTA-VS-Ice"
export PATH=$PATH:$UI_DIR:$SCRIPTS_DIR
export PYTHONPATH=$PYTHONPATH:$UI_DIR:$SCRIPTS_DIR
echo $PATH
sleep 5

nohup python3.6 $UI_DIR/native_ui.py &

sleep 30
#trap "trap_ctrlc" 2
curl --max-time 10 localhost:5002/location=run
curl --max-time 10 localhost:5010/location=run
nohup python3 $SCRIPTS_DIR/Server.py &
#trap "trap_ctrlc" 2
sleep 1
nohup python3 $SCRIPTS_DIR/Client.py &

#trap "trap_ctrlc" 2

