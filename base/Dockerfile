# Base image dockerfile for sdv
FROM ubuntu:bionic
WORKDIR /opt
COPY ./setup_base.sh .
RUN chmod +x setup_base.sh
RUN bash setup_base.sh
RUN echo "source /opt/OpenDDS/setenv.sh" >> ~/.bashrc
#RUN rm setup_base.sh
RUN mkdir .setup &&  mv setup_base.sh ./.setup
 
