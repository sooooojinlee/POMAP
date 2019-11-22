# POMAP :robot:
## 실내 정보를 자동으로 인식하고 바뀐 정보를 스스로 업데이트하는 인공지능 로봇

#### 프로젝트 주요 이슈 :dart:
1. 공간전체정보인식을 어떻게 할 것 인가, 터틀봇 제어 문제
 * 2DLidar 기반 RPLidar 사용
2. 인식한 전체 공간 정보에서 구역 인식(?)
 * SLAM 맵핑 정보와 웹캠으로 인식한 이미지 정보와 비교(?)
3. 간판의 변화 감지(POI 변화 인식 문제)
 * 


#### REFERENCE :file_cabinet:
| TITLE | URL |
| ----- | -------- |
| 셀프 업데이팅 맵 - 딥러닝을 활용한 실내 매장 변화 검출 알고리즘 개발기 | https://www.naverlabs.com/storyDetail/131 |
| AVER LABS' Indoor Dataset - COEX POI Change Detection (Jun. 2018 and Sep. 2018) | https://www.naverlabs.com/en/storyDetail/125 |
| 고정밀 지도를 자동으로 업데이트하는 기술 | https://www.naverlabs.com/storyDetail/139 |
| 로봇이 보는 세상, 매핑로봇 M1X | https://www.naverlabs.com/storyDetail/138 |
| AI관련 논문과 코드를 같이 볼 수 있는 사이트 | https://paperswithcode.com/ |
| SLAM Dataset | http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html |
| IROS2019 SLAM 관련 논문 정리 | http://jinyongjeong.github.io/2019/11/07/IROS2019_SLAM_list/ |
| RPLidar Hector SLAM | https://github.com/NickL77/RPLidar_Hector_SLAM |
| hector_slam | https://github.com/tu-darmstadt-ros-pkg/hector_slam |
| Google Cloud Vision API | https://cloud.google.com/vision/docs/features-list?refresh=1 |





#### 191120 
* ROS Rviz 에 camera 노드 생성함 
 * 웹캠이랑 연결
* ROS Rviz에 rplidar 노드 만들어서 점군 이미지 띄우기 시도중
  * ttyUSB0라는 포트가 없음 -> 포트이름 바꿔도 안됨
* KOBUKI 구입->재고확인 안됨
* Donkey car ssh 통신 문제

#### 191121
* RPLidar 드라이버 깔고 work station 사망함
* 터틀봇 다음주에 옴
* OCR로 문자 인식 시도함
 * 간판인식과는 거리가 먼 알고리즘이라 판단
* YOLO
 * 이미지 인식을 통해 객체를 구분하여 라벨링하는 것까지 성공했으나 동영상과 웹캠 실행의 오류 문제가 생김
 * 동영상 인식을 위해 CUDA 및 openCV 재설치 중에 시스템 오류발생 / 문제해결 

#### 191122
