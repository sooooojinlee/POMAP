# !/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty
from sensor_msgs.msg import LaserScan
import time
import cv2

BURGER_MAX_LIN_VEL = 0.17 # 터틀봇의 직선 속도 상한선
BURGER_MAX_ANG_VEL = 2.84 # 터틀봇의 회전 속도 상한선

LIN_VEL_STEP_SIZE = 0.01 # 키 입력 모드 시, 키 입력 1번당 변화하는 직선 속도
ANG_VEL_STEP_SIZE =0.1 # 키 입력 모드 시, 키 입력 1번당 변화하는 회전 속도

msg = """
Select your own direction.
---------------------------
Moving around:
        w
    a   s   d
        x
    w/x : increase/decrease linear velocity
    a/d : increase/decrease angular velocity
    space key, s : force stop
    
    CTRL-C to quit
"""

caution = """
Velocity is too high
"""

## 장애물 인식에 필요한 Obstacle 클래스 선언
class Obstacle():
    def __init__(self): # Call the init func, when making new instance.
        self.LIDAR_ERR = 0.05 # 측정할 거리의 최소값을 설정
        self._cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1) # Twist 메세지 타입을 사용하는 'cmd_vel'토픽에게 노드를 발행
        self.obstacle() 

    def obstacle(self): 
        self.twist = Twist() # Twist()선언. linear(x, y, z)와 angular(x, y, z)를 인자로 가짐
        while not rospy.is_shutdown(): # ctrl-c 누르기 전까지는 무한 루프
            msg = rospy.wait_for_message("/scan", LaserScan) # wait_for_message -> 토픽에 대한 새 subscribe를 만들고, 1개의 메시지를 수신하면 subscribe 파기
            self.scan_filter = [] # 센서로부터 오는 거리 값을 저장할 scan_filter 생성
            
            for i in range(360):
                if i <= 45 or i > 315: # 센서값을 저장할 로봇 전방 각도 범위 지정. (정면으르 0으로 정하였을 때, 좌우 45도씩 스캔)
                    if msg.ranges[i] >= self.LIDAR_ERR: # 측정한 거리 값이 LIDAR_ERR보다 크면
                        self.scan_filter.append(msg.ranges[i]) # scan_filter에 거리 값을 저장
            
            if min(self.scan_filter) < 0.10: # 센서로부터 들어온 거리값(scan_filter)이 0.10보다 작으면
                self.twist.linear.x = 0.00 # 직선 속도를 0으로
                self.twist.angular.z = 0.0 # 회전 속도를 0으로 설정
                self._cmd_pub.publish(self.twist) # 이전에 선언한 cmd_pub로 하여금 twist라는 인수를 'cmd_vel'에 값을 전함
                rospy.loginfo('Stop!') # 터미널에 Stop 출력, 노드의 로그 파일에 기록 및 rosout에 기록
                break # End-of-while

            else: # 센서로부터 들어온 거리값이 0.10보다 크면
                self.twist.linear.x = 0.00 # 직선속도
                self.twist.angular.z = 0.0 # 회전속도
                rospy.loginfo('distance of the obstacle : %f', min(self.scan_filter)) # 현재 전방 범위 내에서 가장 가까운 장애물과의 거리값을 터미널에 표시
                rospy.loginfo(time.time()) # 현재 시간 표시

            self._cmd_pub.publish(self.twist)


    def getKey(): # 키 입력을 받을 함수 getKey() 선언
        tty.setraw(sys.fileno()) # fileno()를 raw로 전환, fileno()는 스트림의 기본이 되는 file descripter를 반환하는 함수
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1) # 시스템 호출 관련 인터페이스. 첫번째 인자는 입력 관련. 중간 2개는 출력, 에러 관련. 0.1은 딜레이
        if rlist:
            key = sys.stdin.read(1) # 입력한 키를 읽은 후, key에 저장
        else:
            key = ''

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) # stdin의 에코를 끄고, 표준모드를 비활성화
        return key
        


    def vels(target_linear_vel, target_angular_vel): # 목표 속도값을 리턴하는 함수. 키 입력 시 표시될 예정
        return "currentle:\tlinear vel %s\t angular vel %s " % (target_linear_vel, target_angular_vel)
    

    def Calculate_vel(output, input, slop): # output : 현재속도, input : 목표속도, slop : LIN_VEL_STEP_SIZE/2가 대입되어 사용될 함수, 현재 속도 결정
        if input > output: # 전진
            output = min(input, output + slop)
        elif input < output: # 후진
            output = max(input, output - slop)
        else:
            output = input
        return output

    def constrain(input, low, high): # input을 상한, 하한값과 비교한 후, 알맞은 값을 대입하는 함수
        if input < low:
            input = low
        elif input > high:
            input = high
        else:
            input = input
        return input

    def check_LIN_limit_VEL(vel): # 속도의 최대, 최저값과 속도(vel)를 비교함
        vel = constrain(vel, -BURGER_MAX_LIN_VEL, -BURGER_MAX_LIN_VEL) # 목표속도가 BURGER_MAX_LIN_VEL보다 빠르면, 목표속도에 BURGER_MAX_LIN_VEL를 대입하여 목표속도를 제한

        return vel

    def check_ANG_limit_VEL(vel):
        vel = constrain(vel, -BURGER_MAX_ANG_VEL, -BURGER_MAX_ANG_VEL)

        return vel


    if __name__ == "__main__":
        settings = termios.tcgetattr(sys.stdin)

        rospy.init_node('liv') # rospy에게 해당 코드 부분을 알려줌
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10) 

        count = 0 
        whole_count = 0
        status = 0
        target_linear_vel = 0
        target_angular_vel = 0
        control_linear_vel = 0
        control_angular_vel = 0

        try:
            while(1):
                mode_obstacle = Obstacle() # Obstacle() 클래스 선언과 동시에 내부 obstacle 함수 실행
                print(msg)

                while(1):
                    key = getKey() # getKey() 선언으로 키 입력 받을 준비 완료
                
                    if key == 'w': # 전진할 때
                        target_linear_vel = check_LIN_limit_VEL(target_linear_vel + LIN_VEL_STEP_SIZE)
                            # 목표속도를 증가시키기 전, check_LIN_limit_VEL 함수로 최대값을 넘는지 판단
                        status = status + 1 # 키 입력 횟수 카운트
                        print(vels(target_linear_vel, target_angular_vel)) # 목표속도 출력

                        if target_linear_vel == check_LIN_limit_VEL(target_linear_vel + LIN_VEL_STEP_SIZE):
                            # 입력한 목표속도가 최대값을 넘었다면
                            print(caution) # 경고 문구 출력
                            count = count + 1 # 경고 카운트 증가
                            if count == 3 : # 경고 카운트가 3에 다다르면
                                target_linear_vel = target_linear_vel / 2 # 목표속도를 반으로 감소시킴
                                print (vels(target_linear_vel, target_angular_vel))
                                count = 0 # 경고 카운트

                    elif key == 'x': # 후진할 때
                        target_linear_vel = check_LIN_limit_VEL(target_linear_vel - LIN_VEL_STEP_SIZE)
                        status = status + 1
                        print(vels(target_linear_vel, target_angular_vel))

                        if target_linear_vel == check_LIN_limit_VEL(target_linear_vel - LIN_VEL_STEP_SIZE):
                            print(caution)
                            count = count + 1
                            if count == 3 :
                                target_linear_vel = target_linear_vel / 2
                                print (vels(target_linear_vel, target_angular_vel))
                                count = 0

                    elif key == 'a': # 좌회전
                        target_linear_vel = check_LIN_limit_VEL(target_linear_vel + ANG_VEL_STEP_SIZE)
                        status = status + 1
                        print(vels(target_linear_vel, target_angular_vel))
                        if target_linear_vel == check_LIN_limit_VEL(target_linear_vel + ANG_VEL_STEP_SIZE):
                            print(caution)
                            count = count + 1
                            if count == 3 :
                                target_linear_vel = target_linear_vel / 2
                                print (vels(target_linear_vel, target_angular_vel))
                                count = 0

                    elif key == 'd': # 우회전
                        target_linear_vel = check_LIN_limit_VEL(target_linear_vel - ANG_VEL_STEP_SIZE)
                        status = status + 1
                        print(vels(target_linear_vel, target_angular_vel))

                        if target_linear_vel == check_LIN_limit_VEL(target_linear_vel - ANG_VEL_STEP_SIZE):
                            print(caution)
                            count = count + 1
                            if count == 3 :
                                target_linear_vel = target_linear_vel / 2
                                print (vels(target_linear_vel, target_angular_vel))
                                count = 0

                    elif key == 'p' : 
                        rospy.loginfo('distance of the obstacle : %f', min(self.scan_filter))
                            # 키 입력 받으면 현재 장애물과의 거리를 프린트, 에러 발생하는 코드

                    elif key == '' or key == 's' : # 키 입력 받으면 모든 속도를 0으로 전환, 정지하는 키
                        target_linear_vel = 0
                        control_linear_vel = 0
                        target_angular_vel = 0
                        control_angular_vel = 0
                        print (vels(0,0))

                    elif status == 20 : # 키 입력을 20번 하면, 다시 키 입력하면 메시지 프린트, 실험용
                        print (msg)
                        status = 0
                    else :
                        if (key == '\x03') : # ctrl+C 입력받으면 키 입력 모드 종료 및 다시 obstacle() 실행
                            break
                    
                    twist = Twist() # linear, angular를 사용하기 위한 선언. (getKey() 바로 다음 오는 것이 더 자연스러움)

                    control_linear_vel = Calculate_vel(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
                        # 현재속도를 Calculate_vel를 통하여 증가시킴
                    twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z=0.0
                        # 실제 모터의 x축 방향 속도인 twist.linear.vel에 계산된 속도 대입, 나머지 인자들은 0 처리

                    control_angular_vel = Calculate_vel(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
                        # 회전속도를 Calculate_vel를 통하여 증가시킴
                    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

                    pub.publish(twist)

        except : # 예기치 못한 에러 발생시 e를 프린트
            print (e)
        
        finally : # 메인의 반복문 종료 후, 모든 속도 0으로 전환
            twist = Twist()
            twist.linear.x = 0; twist.linear.y = 0 ; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            pub.publish(twist)
        
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)