#!/usr/bin/python3.6
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog , QApplication, QDesktopWidget,QMessageBox, QTableWidget
import test
import sys

from multiprocessing.connection import Client,Listener
#from hvac_proxy import *
import threading
#import pickle
import time
from datetime import timedelta
#import cv2
import base64
import numpy as np
import json
import os
count=0

path="/home/nvidia/HVAC_VS_OD_OTA_v1.7/nativeUI"
os.chdir(path)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("HomeScreen.ui",self)
        self.applications.clicked.connect(self.gotoapplscreen)
        self.applications.setToolTip('Applications')
        self.power.clicked.connect(self.relaunchscreen)

    def relaunchscreen(self):
        os.system("killall xterm")


    def gotoapplscreen(self):
        global otascreen,vsscreen,odscreen,hvacscreen,mclscreen
        otascreen = otaScreen()
        vsscreen = vsScreen()
        odscreen = odScreen()
        #mclscreen = mclScreen()
        widget.addWidget(otascreen)
        widget.addWidget(vsscreen)
        widget.addWidget(odscreen)
        #widget.addWidget(mclscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.show()


class applScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(applScreen,self).__init__()
        loadUi("ApplScreen.ui",self)
        self.ota_button.setEnabled(True)
        self.ota_button.clicked.connect(self.gotootascreen)
        self.mcl_button.setEnabled(False)
        self.vs_button.setEnabled(True)
        self.od_button.setEnabled(True)
        self.vs_button.clicked.connect(self.gotovsscreen)
        self.od_button.clicked.connect(self.gotoodscreen)
        self.home.clicked.connect(self.gotomainscreen)
        self.hvac_button.setEnabled(True)
        self.hvac_button.clicked.connect(self.gotohvacscreen)
        self.sg_button.setEnabled(False)
        self.power.clicked.connect(self.relaunchscreen)
    def relaunchscreen(self):
        os.system("killall xterm")
    def gotootascreen(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotovsscreen(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)
    def gotoodscreen(self):
        widget.setCurrentIndex(widget.currentIndex() + 3)
    def gotohvacscreen(self):
        widget.setCurrentIndex(widget.currentIndex()+ 4)
    def gotomainscreen(self):
        vsscreen.deleteLater()
        odscreen.deleteLater()
        #mclscreen.deleteLater()
        otascreen.deleteLater()
        widget.setCurrentIndex(widget.currentIndex() - 1)
        
        
class otaScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(otaScreen,self).__init__()
        loadUi("OTA_Screen.ui",self)
        count=0

        self.back.clicked.connect(self.gotoapplscreen)
        self.exit.clicked.connect(self.gotoapplscreen)
        self.back.setToolTip("Go Back")
        self.exit.setToolTip("Exit this App")
        self.home.clicked.connect(self.gotomainscreen)
        self.power.clicked.connect(self.relaunchscreen)
        self.power.setToolTip("Restart App!")

        self.Download_Update.setEnabled(False)
        self.install_update.setEnabled(False)
        self.rollback_update.setEnabled(True)

        self.Check_Update.clicked.connect(self.check_update_clicked)
        self.Download_Update.clicked.connect(self.download_update_clicked)
        self.install_update.clicked.connect(self.install_update_clicked)
        self.rollback_update.clicked.connect(self.rollback_clicked)
        self.WorkerOTA = WorkerOTA()
        self.WorkerOTA.start()

        self.WorkerOTA.ota_signal.connect(self.update_table)
        #self.loadData()

    def relaunchscreen(self):
        os.system("killall xterm")

    def stopOTAListen(self):
        self.WorkerOTA.stop()

    def update_table(self,msg):
        print("Inside update table")
        print(msg)
        #print(type(msg))
        dict = json.loads(msg)
        #db = {}
        #db['dict'] = msg
        if (dict['id'] == 1):
            if (dict['update_status'] == "Update available"):
               self.version_table.setItem(0,2,QtWidgets.QTableWidgetItem(dict['old_version_vs']))
               self.version_table.setItem(0,3,QtWidgets.QTableWidgetItem(dict['curr_version_vs']))
               self.version_table.setItem(0,4,QtWidgets.QTableWidgetItem(dict['new_version_vs']))
               self.version_table.setItem(0,5,QtWidgets.QTableWidgetItem(dict['update_status']))
            if (dict['update_status'] == "Update downloaded"):
               self.version_table.setItem(0,5,QtWidgets.QTableWidgetItem(dict['update_status']))
            if (dict['update_status'] == "Update installed"):
               self.version_table.setItem(0,2,QtWidgets.QTableWidgetItem(dict['old_version_vs']))
               self.version_table.setItem(0,3,QtWidgets.QTableWidgetItem(dict['curr_version_vs']))
               self.version_table.setItem(0,4,QtWidgets.QTableWidgetItem("-"))
               self.version_table.setItem(0,5,QtWidgets.QTableWidgetItem(dict['update_status']))
            if (dict['update_status'] == "Update rolledback"):
               self.version_table.setItem(0,2,QtWidgets.QTableWidgetItem("-"))
               self.version_table.setItem(0,3,QtWidgets.QTableWidgetItem(dict['curr_version_vs']))
               self.version_table.setItem(0,4,QtWidgets.QTableWidgetItem("-"))
               self.version_table.setItem(0,5,QtWidgets.QTableWidgetItem(dict['update_status']))         
        if (dict['id'] == 2):
            if (dict['update_status'] == "Update available"):
               self.version_table.setItem(1,2,QtWidgets.QTableWidgetItem(dict['old_version_py']))
               self.version_table.setItem(1,3,QtWidgets.QTableWidgetItem(dict['curr_version_py']))
               self.version_table.setItem(1,4,QtWidgets.QTableWidgetItem(dict['new_version_py']))
               self.version_table.setItem(1,5,QtWidgets.QTableWidgetItem(dict['update_status']))
            if (dict['update_status'] == "Update installed"):
               self.version_table.setItem(1,2,QtWidgets.QTableWidgetItem(dict['old_version_py']))
               self.version_table.setItem(1,3,QtWidgets.QTableWidgetItem(dict['curr_version_py']))
               self.version_table.setItem(1,4,QtWidgets.QTableWidgetItem("-"))
               self.version_table.setItem(1,5,QtWidgets.QTableWidgetItem(dict['update_status']))
            if (dict['update_status'] == "Update rolledback"):
               self.version_table.setItem(1,2,QtWidgets.QTableWidgetItem("-"))
               self.version_table.setItem(1,3,QtWidgets.QTableWidgetItem(dict['curr_version_py']))
               self.version_table.setItem(1,4,QtWidgets.QTableWidgetItem("-"))
               self.version_table.setItem(1,5,QtWidgets.QTableWidgetItem(dict['update_status']))


    def gotoapplscreen(self):
        widget.setCurrentIndex(widget.currentIndex() -1)
    def gotomainscreen(self):
        vsscreen.deleteLater()
        odscreen.deleteLater()
        #mclscreen.deleteLater()
        otascreen.deleteLater()        
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def check_update_clicked(self):
        if self.vs_radio.isChecked() == True:
            print ("vs is selected")
            frame_id=1
            conn_ota.send({'application':'ota', 'frame_id': 1, 'sample' : 'check clicked'})
            #self.version_table.setItem(0,2,QtWidgets.QTableWidgetItem("-"))
            #self.version_table.setItem(0,3,QtWidgets.QTableWidgetItem("1.0"))
            #self.version_table.setItem(0,4,QtWidgets.QTableWidgetItem("1.1"))
            #self.version_table.setItem(0,5,QtWidgets.QTableWidgetItem("Update available"))
        elif self.python_radio.isChecked()==True:
            print ("python is selected")
            frame_id=2
            conn_ota.send({'application':'ota', 'frame_id': 2, 'sample' : 'check clicked' })
        self.Download_Update.setEnabled(True)
        print("check update clicked")

    def download_update_clicked(self):
        if self.vs_radio.isChecked() == True:
            print ("vs is selected")
            frame_id=3
            conn_ota.send({'application':'ota', 'frame_id': 3, 'sample' : 'download clicked' })
            self.version_table.setItem(0,5,QtWidgets.QTableWidgetItem("Download in progress..."))
        elif self.python_radio.isChecked()==True:
            print ("python is selected")
            frame_id=4
            conn_ota.send({'application':'ota', 'frame_id': 4, 'sample' : 'download clicked' })
        self.install_update.setEnabled(True)
        print("download_update_clicked")


    def install_update_clicked(self):

        if self.vs_radio.isChecked() == True:
            print ("vs is selected")
            frame_id=5
            conn_ota.send({'application':'ota', 'frame_id': 5, 'sample' : 'install clicked' })
        elif self.python_radio.isChecked()==True:
            print ("python is selected")
            frame_id=6
            conn_ota.send({'application':'ota', 'frame_id': 6, 'sample' : 'install clicked' })



    def rollback_clicked(self):
        
        if self.vs_radio.isChecked() == True:
            print ("vs is selected")
            frame_id=7
            conn_ota.send({'application':'ota', 'frame_id': 7, 'sample' : 'rollback clicked' })
        elif self.python_radio.isChecked()==True:
            print ("python is selected")
            frame_id=8
            conn_ota.send({'application':'ota', 'frame_id': 8, 'sample' : 'rollback clicked' })
        print("rollback_update_clicked")

    
class WorkerOTA(QtCore.QThread):
    

    ota_signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(WorkerOTA,self).__init__()
        pass



    # def listener_func(self, data: DataType):
    #     print("Cameback from ota")

    #     self.ota_signal.emit(data.sample)


    def run(self):
        self.ThreadActive = True
        # Capture = cv2.VideoCapture('./driving.mp4')

        print(self.ThreadActive)
        # subscriber_ota = domain.create_subscriber()
        # topic_name= 'ota/otaResponse'
        # topic_ota = domain.create_topic(topic_name, DataType)

        # reader_ota = subscriber_ota.create_datareader(topic=topic_ota, listener=self.listener_func)
        # reader_ota.wait_for(StatusKind.SUBSCRIPTION_MATCHED, timedelta(seconds=500))
        # time.sleep(60)
        while self.ThreadActive:
            data_to_display=conn_rec_ota.recv()
            # print(sample)
            # if data:
            print(data_to_display)
            if 'application' in data_to_display and data_to_display["application"] == 'ota':
                sample=data_to_display['data']
                print(sample)
                self.ota_signal.emit(sample)

    def stop(self):
        self.ThreadActive = False
        self.quit()



class vsScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(vsScreen,self).__init__()
        loadUi("video_streaming.ui",self)
        self.back.clicked.connect(self.gotoapplscreen)
        self.exit.clicked.connect(self.gotoapplscreen)
        self.home.clicked.connect(self.gotomainscreen)

        self.play_button.clicked.connect(self.okclicked)
        self.stop_button.clicked.connect(self.cancelclicked)
        self.cam1_radio.setChecked(True)
        self.cam1_radio.clicked.connect(lambda : self.setcamera(1))
        self.cam2_radio.clicked.connect(lambda : self.setcamera(2))
        self.cam3_radio.clicked.connect(lambda : self.setcamera(3))
        self.cam4_radio.clicked.connect(lambda : self.setcamera(4))
        self.commandLinkButton.clicked.connect(self.show_groupbox)
        self.selected_camera=1
        self.Worker1 = Worker1(self.selected_camera)
        self.Worker1.start()

        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        
        # print("workwer initialised")
        

        

    def ImageUpdateSlot(self, Image):
        print("coming--")
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(Image))


    def CancelFeed(self):
        # self.Worker1.stop()
        pass

        

    def update_screen_on_app_signal(self,lis=None):
        if lis is not None:
            print(lis[0])
            print(lis[1])

    def setcamera(self,cam=1):
        self.selected_camera=cam

    def show_groupbox(self):
        self.groupBox.show()

    def okclicked(self):
        print("Ok Clicked")
        print("selected camera {}".format(self.selected_camera))
        self.groupBox.hide()
        
        #send event data to ui_pub for publishing to dds

        conn.send({'application':'vs', 'cam_selected': self.selected_camera, 'action' : 'play' })
        


    def cancelclicked(self):
        print("Canecel Clicked")
        self.groupBox.hide()
        self.CancelFeed()
        conn.send({'application':'vs', 'cam_selected': self.selected_camera, 'action' : 'stop' })

    def gotoapplscreen(self):
        widget.setCurrentIndex(widget.currentIndex() -2)
    def gotomainscreen(self):
        vsscreen.deleteLater()
        odscreen.deleteLater()
        #mclscreen.deleteLater()
        otascreen.deleteLater()
        widget.setCurrentIndex(widget.currentIndex() - 3)

class Worker1(QtCore.QThread):
    

    ImageUpdate = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self,selected_camera=1):
        super(Worker1,self).__init__()
        self.selected_camera =selected_camera
        self.count=0

    # def listener_func(self, sample: DataType):
    #     print("Cameback from microservice")
    #     str1=''
    #     for i in sample.buffer:
    #         str1+=chr(i)

    #     arr=bytes(str1,'utf-8')
    #     decoded=base64.b64decode(arr)
    #     y = np.frombuffer(decoded,dtype=np.uint8)
    #     Image = cv2.imdecode(y, cv2.IMREAD_COLOR)
        
    #     print("count {}".format(self.count))
    #     self.count += 1
    #     Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
    #     FlippedImage = cv2.flip(Image, 1)
    #     ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format_RGB888)
    #     Pic = ConvertToQtFormat.scaled(911, 481, QtCore.Qt.KeepAspectRatio)
    #     self.ImageUpdate.emit(Pic)


    def run(self):
        self.ThreadActive = True
        # Capture = cv2.VideoCapture('./driving.mp4')
        
        print(self.ThreadActive)
        # subscriber1 = domain.create_subscriber()
        # topic_name= 'videoStreaming/camFeed'
        # topic1 = domain.create_topic(topic_name, DataType)

        # reader1 = subscriber1.create_datareader(topic=topic1, listener=self.listener_func)
        # reader1.wait_for(StatusKind.SUBSCRIPTION_MATCHED, timedelta(seconds=500))
        # time.sleep(60)
        while self.ThreadActive:
            data_to_display=conn_rec_vs.recv()
            #print(sample)
            # if data:
            if 'application' in data_to_display and data_to_display['application'] == 'vs':
                Image=data_to_display['image']
                self.count += 1
                print("enter{}".format(self.count))
                # str1=''
                # for i in msg.buffer:
                #     str1+=chr(i)

                # arr=bytes(str1,'utf-8')
                # decoded=base64.b64decode(arr)
                # y = np.frombuffer(decoded,dtype=np.uint8)
                # Image = cv2.imdecode(y, cv2.IMREAD_COLOR)
                
                # # print("count {}".format(self.count))
                
                # Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
                # cv2.imshow('image',Image)
                # cv2.waitKey(1)
                FlippedImage = Image #cv2.flip(Image, 1)
                ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(911, 481, QtCore.Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                print("exit {}".format(self.count))
            
            

            # ret, frame = Capture.read()
            # if ret:
            #     # print("1")
            #     Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #     FlippedImage = cv2.flip(Image, 1)
            #     ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format_RGB888)
            #     Pic = ConvertToQtFormat.scaled(911, 481, QtCore.Qt.KeepAspectRatio)
            #     self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()

class odScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(odScreen,self).__init__()
        loadUi("object_detection.ui",self)
        self.back.clicked.connect(self.gotoapplscreen)
        self.exit.clicked.connect(self.gotoapplscreen)
        self.home.clicked.connect(self.gotomainscreen)

        

        self.play_button.clicked.connect(self.okclicked)
        self.stop_button.clicked.connect(self.cancelclicked)
        self.cam1_radio.setChecked(True)
        self.cam1_radio.clicked.connect(lambda : self.setcamera(1))
        self.cam2_radio.clicked.connect(lambda : self.setcamera(2))
        self.cam3_radio.clicked.connect(lambda : self.setcamera(3))
        self.cam4_radio.clicked.connect(lambda : self.setcamera(4))
        self.commandLinkButton.clicked.connect(self.show_groupbox)
        self.selected_camera=1

        self.WorkerOD = WorkerOD(self.selected_camera)
        self.WorkerOD.start()

        self.WorkerOD.ImageUpdate.connect(self.ImageUpdateSlot)


    def ImageUpdateSlot(self, Image):
        print("coming--")
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(Image))

    def CancelFeed(self):
        # self.Worker1.stop()
        pass
    
    def update_screen_on_app_signal(self,lis=None):
        if lis is not None:
            print(lis[0])
            print(lis[1])

    def setcamera(self,cam=1):
        self.selected_camera=cam

    def show_groupbox(self):
        self.groupBox.show()

    def okclicked(self):
        print("Ok Clicked")
        print("selected camera {}".format(self.selected_camera))
        self.groupBox.hide()
        conn.send({'application':'od', 'cam_selected': self.selected_camera, 'action' : 'play' })


    def cancelclicked(self):
        print("Canecel Clicked")
        self.groupBox.hide()
        self.CancelFeed()
        conn.send({'application':'od', 'cam_selected': self.selected_camera, 'action' : 'stop' })

    def gotoapplscreen(self):
        widget.setCurrentIndex(widget.currentIndex() -3)
    def gotomainscreen(self):
        vsscreen.deleteLater()
        odscreen.deleteLater()
        #mclscreen.deleteLater()
        otascreen.deleteLater()        
        widget.setCurrentIndex(widget.currentIndex() - 4)


class WorkerOD(QtCore.QThread):
    

    ImageUpdate = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self,selected_camera=1):
        super(WorkerOD,self).__init__()
        self.selected_camera =selected_camera
        self.count=0
    


    def run(self):
        self.ThreadActive = True
        
        #while self.ThreadActive:
        #    data_to_display=conn_rec_od.recv()
            
        #    if 'application' in data_to_display and data_to_display['application'] == 'od':
        #        Image=data_to_display['image']
        #        self.count += 1
        #        print("enter{}".format(self.count))
                
        #        FlippedImage = Image  #cv2.flip(Image, -1)
        #        ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format_RGB888)
        #        Pic = ConvertToQtFormat.scaled(911, 481, QtCore.Qt.KeepAspectRatio)
        #        self.ImageUpdate.emit(Pic)
        #        print("exit {}".format(self.count))
            
            

            
    def stop(self):
        self.ThreadActive = False
        self.quit()


####################################FEV##########################################


class hvacScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(hvacScreen,self).__init__()

        self.hvac_proxyPy_obj=hvac_proxyPy()
        self.hvac_proxyPy_obj.set_py_ResponseCallback_temperature(self.hvacscreen_cbk)
        print("HVAC DDS READY")

        loadUi("HvacScreen.ui",self)
        self.back.clicked.connect(self.gotoapplscreen)
        self.exit.clicked.connect(self.gotoapplscreen)
        self.back.setToolTip("Go Back")
        self.exit.setToolTip("Exit this App")
        self.home.clicked.connect(self.gotomainscreen)
        self.power.clicked.connect(self.relaunchscreen)
        self.power.setToolTip("Restart App!")
        self.seats_switch.setEnabled(False)

        #conditions
        self.acSwitch.stateChanged.connect(self.switchingac)
        self.seats_switch.stateChanged.connect(self.selectingseat)
        self.temp_slider.setEnabled(False)
        self.int_circ_switch.setEnabled(False)
        self.seat_sel.setEnabled(False)
        self.temp_slider.valueChanged.connect(self.updateLCD)
        self.fan_low.clicked.connect(self.fan_speed_check)
        self.fan_medium.clicked.connect(self.fan_speed_check)
        self.fan_high.clicked.connect(self.fan_speed_check)

    def updateCabinTemp(self, data):
        self.cabin_temp.display(data)

    def hvacscreen_cbk(self,tempObj):
        self.updateCabinTemp(int(tempObj.temp))
        print("hvacscreen_cbk arrived")

    def fan_speed_check(self):
        if self.fan_low.isChecked():
            print("low")

        elif self.fan_medium.isChecked():
            print("medium")
        elif self.fan_high.isChecked():
            print("high")

    def switchingac(self, state):
        if state == QtCore.Qt.Checked:
            self.temp_slider.setEnabled(True)
            self.int_circ_switch.setEnabled(True)
        else:
            self.temp_slider.setEnabled(False)
            self.int_circ_switch.setEnabled(False)
    def selectingseat(self, state):
        if state == QtCore.Qt.Checked:
            self.seat_sel.setEnabled(True)
        else:
            self.seat_sel.setEnabled(False)
    
    def updateLCD(self, event): ################## callback called when slider slides
        self.hvac_proxyPy_obj.TempObj.temp=str(event)
        self.hvac_proxyPy_obj.TempObj.zone="All"
        py_writeObj=dds_app_py.hvacWriteReqObj(dds_app_py.featureType.TEMPERATURE)
        py_writeObj.messageId="temperature slider update"
        py_writeObj.featureObj.temperatureObj(self.hvac_proxyPy_obj.TempObj)
        self.hvac_proxyPy_obj.hvacLibPy_obj.HVACFnWriteRequest(py_writeObj)
        self.instant_temp_change.display(event)
        #conditions

    def relaunchscreen(self):
        os.system("killall xterm")
    def gotoapplscreen(self):
        widget.setCurrentIndex(widget.currentIndex() -4)
    def gotomainscreen(self):
        vsscreen.deleteLater()
        odscreen.deleteLater()
        #mclscreen.deleteLater()
        otascreen.deleteLater()
        widget.setCurrentIndex(widget.currentIndex() -5)
        


####################################FEV##########################################


# init_opendds(opendds_debug_level=0)
# domain = DomainParticipant(42)

# topic = domain.create_topic('videoStreaming/cameraRequest', DataType)
# publisher = domain.create_publisher()
# writer = publisher.create_datawriter(topic)


# ota_topic = domain.create_topic('ota/otaRequest', DataType)
# ota_publisher = domain.create_publisher()
# ota_writer = publisher.create_datawriter(ota_topic)

#
#2nd way

address_sender = ('localhost', 6000)
conn = Client(address_sender)



#address_sender_od = ('localhost', 6002)
# conn_od = Client(address_sender_od)

address_sender_ota = ('localhost',6005)
conn_ota = Client(address_sender_ota)



# ADDR PORT for Receiving VS from ui_sub

address_receiver_vs=('localhost',6001)
#address_receiver_od=('localhost',6002)
address_receiver_ota =('localhost',6006)
listener_vs = Listener(address_receiver_vs)
#listener_od = Listener(address_receiver_od)
listener_ota = Listener(address_receiver_ota)
conn_rec_vs = listener_vs.accept()
#conn_rec_od = listener_od.accept()
conn_rec_ota = listener_ota.accept()





# reader1.wait_for(StatusKind.PUBLICATION_MATCHED, timedelta(seconds=1000))
# topic2 = domain.create_topic('DownloadUpdate', DataType)
# publisher2=domain.create_publisher()
# writer2 = publisher2.create_datawriter(topic2)

# topic3 = domain.create_topic('InstallUpdate', DataType)
# publisher3=domain.create_publisher()
# writer3 = publisher2.create_datawriter(topic3)

# topic4 = domain.create_topic('Rollback', DataType)
# publisher4=domain.create_publisher()
# writer4 = publisher2.create_datawriter(topic4)


# Wait for Publisher to Connect
# print('Waiting for Subscriber...')
# writer.wait_for(StatusKind.PUBLICATION_MATCHED, timedelta(seconds=60))

app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()

mainwindow = MainWindow()
applscreen = applScreen()
#otascreen = otaScreen()
#vsscreen = vsScreen()
#odscreen = odScreen()

#hvac_proxyPy_obj=hvac_proxyPy()

#hvacscreen = hvacscreen()

widget.addWidget(mainwindow)
widget.addWidget(applscreen)
#widget.addWidget(otascreen)
#widget.addWidget(vsscreen)
#widget.addWidget(odscreen)
#widget.addWidget(hvacscreen)

#py_writeObj.messageId="temperature slider update"
#py_writeObj.featureObj.temperatureObj(temperature_obj)
#hvac_proxyPy_obj.HVACFnWriteRequest(py_writeObj)

widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")


