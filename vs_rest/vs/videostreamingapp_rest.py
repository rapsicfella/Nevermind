from flask import Flask, request,render_template, Response
import requests
import threading


import cv2
import base64
import numpy as np
import json
import os

app = Flask(__name__)


class VideoStreamer(object):
    def __init__(self):

        self.action_id =0
        self.params = ''
        
        #11/11
        self.stopthread_1=False
        self.stopthread_2=False
        self.stopthread_3=False
        self.stopthread_4=False

        self.videothread_1=None
        self.videothread_2=None
        self.videothread_3=None
        self.videothread_4=None

        self.VS_CAMFEED_API_ENDPOINT = 'http://192.168.1.11:5020/videoStreaming/camFeed'
        #self.VS_CAMFEED_API_ENDPOINT = 'http://dds.k3s.external/videoStreaming/camFeed'


        
    def stream_video_1(self):
        self.selected_camera =1
       
        cap= cv2.VideoCapture('./york.mp4')
        while(cap.isOpened()):
            ret, frame = cap.read()
            if type(frame) == type(None):
                print("!!! Couldn't read frame!")
            if ret == False:
                break

            if self.stopthread_1:
                break

            # #read frames from mp4 in .jpg file format
            retval, jpgframe = cv2.imencode('.jpg', frame)
            # # #encode jpgframe in base64 format
            encoded_im = base64.b64encode(jpgframe)
            # print(encoded_im)

            encoded_im_str=str(encoded_im,'utf-8')
            
            data = {'action_id':self.action_id,'params':self.params,'data':encoded_im_str}
            r =requests.post(url = self.VS_CAMFEED_API_ENDPOINT, data =json.dumps(data),headers={'Content-type': 'application/json'})
            
            # {'Content-type': 'multipart/form-data'}


        cap.release()
        print("Done closed cap")
        

    def stream_video_2(self):
        print("stream video2")

        self.selected_camera =2
       
        cap= cv2.VideoCapture('./dash.mp4')
        while(cap.isOpened()):
            ret, frame = cap.read()
            if type(frame) == type(None):
                print("!!! Couldn't read frame!")
            if ret == False:
                break

            if self.stopthread_2:
                break

            # #read frames from mp4 in .jpg file format
            retval, jpgframe = cv2.imencode('.jpg', frame)
            # # #encode jpgframe in base64 format
            encoded_im = base64.b64encode(jpgframe)
            # print(encoded_im)

            encoded_im_str=str(encoded_im,'utf-8')
            
            data = {'action_id':self.action_id,'params':self.params,'data':encoded_im_str}
            r =requests.post(url = self.VS_CAMFEED_API_ENDPOINT, data =json.dumps(data),headers={'Content-type': 'application/json'})
            
            # {'Content-type': 'multipart/form-data'}


        cap.release()
        print("Done closed cap")
        

    def stream_video_3(self):
        print("stream video3")
        self.selected_camera =3
       
        cap= cv2.VideoCapture('./studio.mp4')
        while(cap.isOpened()):
            ret, frame = cap.read()
            if type(frame) == type(None):
                print("!!! Couldn't read frame!")
            if ret == False:
                break

            if self.stopthread_3:
                break

            # #read frames from mp4 in .jpg file format
            retval, jpgframe = cv2.imencode('.jpg', frame)
            # # #encode jpgframe in base64 format
            encoded_im = base64.b64encode(jpgframe)
            # print(encoded_im)

            encoded_im_str=str(encoded_im,'utf-8')
            
            data = {'action_id':self.action_id,'params':self.params,'data':encoded_im_str}
            r =requests.post(url = self.VS_CAMFEED_API_ENDPOINT, data =json.dumps(data),headers={'Content-type': 'application/json'})
            
            # {'Content-type': 'multipart/form-data'}


        cap.release()
        print("Done closed cap")

    def stream_video_4(self):
        print("stream video4")
        
        self.selected_camera =4
       
        cap= cv2.VideoCapture('./dark.mp4')
        while(cap.isOpened()):
            ret, frame = cap.read()
            if type(frame) == type(None):
                print("!!! Couldn't read frame!")
            if ret == False:
                break

            if self.stopthread_4:
                break

            # #read frames from mp4 in .jpg file format
            retval, jpgframe = cv2.imencode('.jpg', frame)
            # # #encode jpgframe in base64 format
            encoded_im = base64.b64encode(jpgframe)
            # print(encoded_im)

            encoded_im_str=str(encoded_im,'utf-8')
            
            data = {'action_id':self.action_id,'params':self.params,'data':encoded_im_str}
            r =requests.post(url = self.VS_CAMFEED_API_ENDPOINT, data =json.dumps(data),headers={'Content-type': 'application/json'})
            
            # {'Content-type': 'multipart/form-data'}


        cap.release()
        print("Done closed cap")

    def start_thread_on_request(self,data):
        self.params = data['params']
        params_dict = json.loads(data['params'])
        
        self.videothread_1 = threading.Thread(target=self.stream_video_1,args=())
        self.videothread_2 = threading.Thread(target=self.stream_video_2,args=())
        self.videothread_3 = threading.Thread(target=self.stream_video_3,args=())
        self.videothread_4 = threading.Thread(target=self.stream_video_4,args=())
        self.action_id =0
        if params_dict['action'] =='play':
            if params_dict['id'] == 1:
                self.stopthread_1=False
                self.stopthread_2=True
                self.stopthread_3=True
                self.stopthread_4=True

                self.videothread_1.start()

            if params_dict['id'] == 2:
                self.stopthread_1=True
                self.stopthread_2=False
                self.stopthread_3=True
                self.stopthread_4=True

                self.videothread_2.start()


            if params_dict['id'] == 3:
                self.stopthread_1=True
                self.stopthread_2=True
                self.stopthread_3=False
                self.stopthread_4=True

                self.videothread_3.start()


            if params_dict['id'] == 4:
                self.stopthread_1=True
                self.stopthread_2=True
                self.stopthread_3=True
                self.stopthread_4=False

                self.videothread_4.start()


        elif params_dict['action'] =='stop':

                self.stopthread_1=True
                self.stopthread_2=True
                self.stopthread_3=True
                self.stopthread_4=True



        

@app.route('/videoStreaming/cameraRequest',methods=['POST', 'GET'])
def receive_response_from_gateway():
    # data =request.get_data()
    data =request.get_json()
    print(type(data))
    print(data)
    vs.start_thread_on_request(data)


    return "UI request sent to Microservice Successfully"




if __name__ == "__main__":
    vs = VideoStreamer()
    app.run(host='0.0.0.0', port=5001,threaded=True)
