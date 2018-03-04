FROM don41382/rpi-python3-with-bluetooth
RUN apt update
RUN apt install python-pip python-bluez
RUN pip install paho-mqtt
ADD beacon-py.tar /root
ADD beacon-py /root
WORKDIR /root
