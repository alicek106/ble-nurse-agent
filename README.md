# 간호 대학 요양원 단기 프로젝트
---
### **라즈베리파이 기반의 비콘 감지**

> #### Prerequisite
>  * 라즈베리파이 3

>  * 리니어블 밴드

>  * 도커 컨테이너

### How to use

>  wget -qO- get.docker.com | sh

---
>  docker run -d --net=host --restart=always alicek106/ble-nurse-project:0.3 \
python alicek106-20180304.py BROKER_IP PY01 15
