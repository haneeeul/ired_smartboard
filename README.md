## 적외선 카메라를 이용한 전자칠판 프로그램 개발:
### Development of Electronic Blackboard Program Using Infrared Camera
---

적외선 카메라 모듈과 직접 제작한 IRED 펜을 이용한 전자칠판 개발 프로젝트

* [개요 및 소개](#개요_및_소개)

* [H/W 구성 요소](#H/W_구성_요소)

* [Required](#Required)

* [Command](#Command)

* [활용방안](#활용방안)
<br><br>
### 개요 및 소개

![스마트 칠판 구성도](https://user-images.githubusercontent.com/48266672/120613477-3dbc8880-c491-11eb-8eaa-b8b1c903cc12.png)

라즈베리파이 보드에 연결된 적외선 카메라가 움직이는 적외선 펜의 불빛을 인식해 해당 좌표를 컴퓨터로 전송한다.

전달된 좌표를 이용해 컴퓨터에서 문서 위에 선을 그리는 동작을 수행한다.

<br>

### H/W 구성 요소

![image](https://user-images.githubusercontent.com/48266672/120614846-a1938100-c492-11eb-97d0-d57f2a8791c4.png)

라즈베리파이 보드에 적외선 카메라를 연결한 모습(좌)

자체 제작 적외선 펜을 위해 IRED 다이오드에 전지를 조립한 상태(우)

<br>

### __Required__
프로그램 실행을 위한 버전과 운영체제를 반드시 확인하세요.

    python >= 3.x
    opencv >= 4.x


    /socket/server_win.py: Linux
    /main.py: raspberry pi3
<br>

### __Command__
프로그램 실행을 위한 명령어입니다.

First of all, check IP address of PC. (below xxx.xxx.xxx.xxx)

    python3 server_win.py (default port number: 8090) // PC command
    python3 main.py xxx.xxx.xxx.xxx 8090 // RPI command
<br>

### 활용방안
1. 빔프로젝터 없이 사용한다면 개인용 전자칠판으로 사용 가능.
2. 소규모 강의를 위한 저가의 전자칠판으로 활용 가능.
3. 교육 인프라가 잘 구축되지 않은 곳에서 저가의 전자칠판으로 활용 가능.
