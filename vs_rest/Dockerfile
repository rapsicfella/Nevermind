FROM ubuntu:bionic
WORKDIR /opt
COPY ./setup_vs.sh .
COPY ./requirements.txt .
COPY vs vs
RUN chmod +x setup_vs.sh
RUN bash setup_vs.sh
RUN mv setup_vs.sh ./.setup
RUN mv requirements.txt ./.setup
EXPOSE 5001
WORKDIR /opt/vs/
RUN chmod +x startup.sh 
CMD ["./startup.sh"]
