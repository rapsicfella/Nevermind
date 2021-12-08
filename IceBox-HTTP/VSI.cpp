//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#include <Ice/Ice.h>
#include <VSI.h>

//http requirements
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>	
#include <unistd.h>

#define PORT 8080

using namespace std;

void VSI::initVideoStreamingApp(const Ice::Current&)
{
    
    //sleep(1);
    int sock = 0; long valread;
    struct sockaddr_in serv_addr;
    //char *hello = "Hello from client";
    char buffer[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return;
    }
    
    memset(&serv_addr, '\0', sizeof(serv_addr));
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    
    // Convert IPv4 and IPv6 addresses from text to binary form
    if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)
    {
        printf("\nInvalid address/ Address not supported \n");
        return;
    }
    
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return;
    }
    //send(sock , hello , strlen(hello) , 0 );
    system("python3 /home/harsha/Desktop/Videostreaming_v1/nativeUI_vs/native_ui.py &");
    printf("UI running\n");
    
    //cout.flush();
    //valread = read( sock , buffer, 1024);
    //printf("%s\n",buffer );
}
