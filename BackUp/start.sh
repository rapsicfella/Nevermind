#! /bin/bash



# CONTAINER NAMES FOR THE APPLICATIONS
VS_CONTAINER_NAME=vs_application
HVAC_CONTAINER_NAME=hvac_application
OTA_CONTAINER_NAME=ota_application
trap "trap_ctrlc" 2



function trap_ctrlc ()
{
# perform cleanup here
echo " Ctrl-C caught... Performing clean up"



echo "Exiting..."



# exit shell script with error code 2
# if omitted, shell script will continue execution
docker stop $VS_CONTAINER_NAME $HVAC_CONTAINER_NAME
docker stop $OTA_CONTAINER_NAME
kill -9 $(ps -ef | grep " python" | awk '{print $2}')
mv nohup.out nohup.out.$(date +%s)
exit 2
}



# Start the dockerized applications
docker run -d --rm --net=host --name $VS_CONTAINER_NAME sdv-vs:latest
docker run -d --rm --net=host --name $HVAC_CONTAINER_NAME sdv-hvac:latest
docker run -d --rm --net=host -v /home/nvidia/IVI_UI/nativeUI:/opt/ota/OTA_code/nativeUI \
--name $OTA_CONTAINER_NAME sdv-ota:latest



IVI_UI_FOLDER_PATH=$PWD
echo "UI Folder Path - " $IVI_UI_FOLDER_PATH
source $IVI_UI_FOLDER_PATH/pydds/bin/activate



cd $IVI_UI_FOLDER_PATH/UI_pubSub/ui_pub_sub
python3.8 ui_pub_integrated.py &
sleep 2



cd $IVI_UI_FOLDER_PATH/nativeUI
python3 native_ui.py &
sleep 1



cd $IVI_UI_FOLDER_PATH/UI_pubSub/ui_pub_sub
python3.8 ui_sub_integrated.py &
sleep 1.5



cd $IVI_UI_FOLDER_PATH/Ice-sdv
python3.8 Server_Ice.py &
sleep 1



python3.8 Client_Ice.py &



sleep 99999999999999999999999999999999999999999
