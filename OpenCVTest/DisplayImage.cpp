#include <stdio.h>
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

int main(int argc, char** argv )
{
    VideoCapture cap("../dash.mp4");
    if(!cap.isOpened()){
      cout << "Error opening video stream or file" << endl;
      return -1;
    }
    
    //save video output
    int frame_width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    int frame_height = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    
    VideoWriter video("../outcpp.avi", cv::VideoWriter::fourcc('M','J','P','G'), 30, Size(frame_width,frame_height));
    
    
    
    //
    
   std::string window_name = "Streaming ..";
   cv::namedWindow(window_name, 0); //cv::WINDOW_AUTOSIZE
   cv::resizeWindow(window_name, 800, 600);  
   std::string path = "../Messenger/video_frames/";
   string file;
   int ind = 0;
   while(1){
     Mat frame;
     cap >> frame;
     if(frame.empty()) break;
      std::vector<unsigned char> buffer;
      imencode(".jpg", frame, buffer);
      size_t imgSize = buffer.size();
      unsigned char bfr[imgSize+1];
      for(int i = 0; i < imgSize; i++){
      	bfr[i] = buffer[i];
      }
      //transportation in between
      std::vector<unsigned char> buffer1;
      for(int i = 0; i < imgSize; i++){
        buffer1.push_back(bfr[i]);
      }
      cv::Mat de = cv::imdecode(buffer1, 1);
     file = path + to_string(ind) + ".jpg";
     imshow(window_name, de);
     video.write(de);
     imwrite(file, de);
     waitKey(60);
     ind++;
   }
   
   cap.release();
   video.release();
   destroyAllWindows();
   return 0; 
 }
