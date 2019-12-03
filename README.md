# POMAP :robot:
## 실내 정보를 자동으로 인식하고 바뀐 정보를 스스로 업데이트하는 인공지능 로봇

#### 프로젝트 주요 이슈 :dart:
1. 공간전체정보인식을 어떻게 할 것 인가, 터틀봇 제어 문제
 * 2DLidar 기반 RPLidar 사용
 * 카메라 캘리브레이션 개념
 * SLAM 모르겠음
 * 터틀봇에 달린 센서 많음(웹캠 2대, 파이카메라 1대, RPLidar 1대 등) 
  * 라즈베리파이 어떻게 효율적으로 쓸지 -> 자문 구하기
2. 인식한 전체 공간 정보에서 구역 인식
 * SLAM 맵핑 정보와 웹캠으로 인식한 이미지 정보와 비교
3. 간판의 변화 감지(POI 변화 인식 문제)
 * d(A, P)가 크고 d(A, N)가 작은 어려운 Train dataset 만들기 


#### REFERENCE :file_cabinet:
| TITLE | URL |
| ----- | -------- |
| 셀프 업데이팅 맵 - 딥러닝을 활용한 실내 매장 변화 검출 알고리즘 개발기 | https://www.naverlabs.com/storyDetail/131 |
| NAVER LABS' Indoor Dataset - COEX POI Change Detection (Jun. 2018 and Sep. 2018) | https://www.naverlabs.com/en/storyDetail/125, https://europe.naverlabs.com/blog/making-maps-evergreen/ |
| 고정밀 지도를 자동으로 업데이트하는 기술 | https://www.naverlabs.com/storyDetail/139 |
| 로봇이 보는 세상, 매핑로봇 M1X | https://www.naverlabs.com/storyDetail/138 |
| AI관련 논문과 코드를 같이 볼 수 있는 사이트 | https://paperswithcode.com/ |
| SLAM Dataset | http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html |
| IROS2019 SLAM 관련 논문 정리 | http://jinyongjeong.github.io/2019/11/07/IROS2019_SLAM_list/ |
| RPLidar Hector SLAM | https://github.com/NickL77/RPLidar_Hector_SLAM |
| hector_slam | https://github.com/tu-darmstadt-ros-pkg/hector_slam |
| Google Cloud Vision API | https://cloud.google.com/vision/docs/features-list?refresh=1 |


### 
<details>
 <summary> :calendar: 진행상황</summary>
<div markdown="1">

#### 191120 수
* ROS Rviz 에 camera 노드 생성함 
 * 웹캠이랑 연결
* ROS Rviz에 rplidar 노드 만들어서 점군 이미지 띄우기 시도중
  * ttyUSB0라는 포트가 없음 -> 포트이름 바꿔도 안됨
* KOBUKI 구입->재고확인 안됨
* Donkey car ssh 통신 문제

#### 191121 목
* RPLidar 드라이버 깔고 work station 사망함
* 터틀봇 다음주에 옴
* OCR로 문자 인식 시도함
 * 간판인식과는 거리가 먼 알고리즘이라 판단
* YOLO
 * 이미지 인식을 통해 객체를 구분하여 라벨링하는 것까지 성공했으나 동영상과 웹캠 실행의 오류 문제가 생김
 * 동영상 인식을 위해 CUDA 및 openCV 재설치 중에 시스템 오류발생 / 문제해결 

#### 191122 금
* 3차 중간발표


#### 191126 화
* 터틀봇3 도착해서 조립함
* pytorch로 triplet [잘 돌아가는지 봄](https://github.com/CoinCheung/triplet-reid-pytorch)
* 맵핑할 공간 세트 정의하기(NaverLABS cvpr2019 Did it change? Learning to Detect Poit-of-Interest Changes for Proactive Map Updates 논문 보기 시작하면서 세트 상황 ) 


#### 191127 수
* 라즈베리파이에 ros설치 시도 중(boost error, j1 error남)
* 센서 데이터 처리 어떻게 해야할지 ROS 튜토리얼이랑 비슷한 프로젝트 소스코드 보면서 공부하고 있음
* 라이다로 맵핑한 지도와 매장 위치 정보, 업데이트 정보 어떻게 합치고 랜더링할지 방법 생각함 


#### 191128 목
* 윤은영 교수님 피드백 -> 라이다 지도와 이미지 위치를 연동할 논문 찾아보라 하심


#### ~191202 월 까지 내가 한 일(trello backup 용)


* 라즈베리파이 한번 밀었음(191202)
* 트렐로 내 카드도 밀림 :innocent:
  * 깃에도 빠짐없이 기록하기로,,  
* Remote PC 와 라즈베리파이에 ROS 설치 및 라즈베리파이 기본 설정 후 각 PC에 
```$ sudo apt-get install ssh```
or
```$ sudo apt-get install openssh-server```
둘 다 설치해 봄

* Remote PC와 라즈베리파이 모두 
```/etc/ssh/ssh_config```
```/etc/ssh/sshd_config```  파일 모두 Port 22 주석 처리 해제하기
gedit으로 편집하면 비교적(?) 편하지만 라즈베리파이는 gedit 편집기 안됨

* 위 파일 저장하고 
```service sshd restart``` 
ssh 서비스를 재시작

* 라즈베리파이에서 
```$ sudo systemctl enable ssh```
```$ sudo systemctl start ssh``` 하고  
```$ ssh pirl@192.168.0.15``` 입력하고 패스워드 입력하면 ssh 통신 될 거임  

* 라즈베리파이에서 bringup 시도 했을 때  
[ERROR] unable to contact master at [localhost:11311] 
the traceback for the exception was written to the log file  
이 오류가 뜨는 이유가 OpenCR 펌웨어 업데이트 때문이라는 ROS wiki의 글을 보고 시도해 봤으나 여전히 안되고 topic 메시지들이 전송이 안됨

**Remote PC와 라즈베리파이는 같은 라우터의 네트워크를 공유해야함**

##### 여기까지 설정이 끝났다면 bringup 시도하기

1. Remote PC [terminal 1]
``` $ roscore```  


2. 라즈베리파이
``` $ roslaunch turtlebot3_bringup turtlebot3_robot.launch```  
여기서 publisher, subscriber 메세지 송수신 되야함


3. Remote PC
``` $ export TURTLEBOT3_MODEL=burger``` [terminal 2]
``` $ roslaunch turtlebot3_bringup turtlebot3_remote.launch```[terminal 3]
``` $ rosrun rviz rviz -d `rospack find turtlebot3_description`/rviz/model.rviz ```  
실행했을 때 오류생기는 노드 모두 없어야 함


* 원격 작동(키로 터틀봇 제어하기)
``` $ export TURTLEBOT3_MODEL=burger```
``` $ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch```

여기까지 꼭 해보기


</div>
</details>




