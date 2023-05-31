# Zeronet 모니터링 시스템

탈중앙화 웹인 Zeronet 모니터링 및 ML기반의 IDS시스템



## 🖥️ 프로그램 소개

탈중앙화 웹인 Zeronet의 트래픽을 모니터링을 제시하기 위한 시스템 입니다.

- 시스템 구성도

  <p text-align=center>
  	<img width = "500" alt="시스템구성" src="https://github.com/Greedun/2022_Capstone/assets/78598657/6c7c9f7a-b988-475f-86a1-d7099232d77d">
  </p>

- 개발 의도
  : 탈중앙화웹은 접속한 피어라면 누구든지 서비스를 이용가능하지만
  접속한 피어의 정보가 전부 노출되기 때문에 DoS공격에 악용될 여지가 있습니다.
  따라서 접속 기록을 수집하여 보여주는 모니터링 시스템과 트래픽을 분석하여 경고하는 IDS시스템을 제안하고자 합니다.

<br><br>

## 🕰️ 개발 기간

- 2022.04 ~ 2022.11



## 멤버구성

- 팀장 : 최성현 - 패킷 캡쳐 및 IDS 시스템 개발
- 팀원 : 김소연 - 모니터링 시스템(백엔드), ML 특징 추출
- 팀원 : 정희진 - 모니터링 시스템(프론트엔드)



### ⚙️ 개발 환경

- FrontEnd : javascript, d3(라이브러리)
- BackEnd : django
- IDS : flask, ML(RandomForest)

<br><br>

## 📌 주요 기능

(1) 전세계 접속 피어 확인

<p text-align=center>
  <img width=900 alt="메인페이지" src="https://github.com/Greedun/2022_Capstone/assets/78598657/6f2dfaff-7e83-4f76-b779-cb3da379e2f3">
</p>

운영페이지에 접속시 peer(사용자)의 접근정보가 기록되는데 
기록된 정보를 관리하여 사이트에 접근하는 피어에 대한 정보를 알 수 있다.

<빨간점 : 본인, 노란점 : 정보가 노출되는 peer, 흰점 : 접속기록이 있는 peer >

<br><br>

(2) 트래픽 통계 

<p text-align=center>
  <img width=50% alt="통계 페이지" src="https://github.com/Greedun/2022_Capstone/assets/78598657/2d7424e6-6948-471e-9b68-97f9df236911">
</p>

접속하는 패킷을 수집하고 통계내어 이후 분석에 유용하게 시각화 

(확인 가능한 정보)
=> 날짜별 트래픽, 나라별 트래픽, 프로토콜별 분포도, 하루 시간대별 트래픽, 
     ip별 송수신 갯수, 토르 브라우저 사용 유무

<br>

<br>

(3) IDS 작동

<p text-align=center>
  <img width="838" alt="IDS작동" src="https://github.com/Greedun/2022_Capstone/assets/78598657/486a4ac3-a897-4499-93b8-e06c6aa10ffe">
</p>

(동작 과정)

1. 5분간 수집한 패킷을 csv형태로 저장

2. 학습된 모델에 데이터를 넣고 판단
3. 악성으로 판단된 ip가 있다면 경고창 띄움
4. 이후 관리자가 해당 ip에 대한 분석후 악성으로 판단시 block처리

<br>

(네트워크 특징 기준)

- 1차 기준 : 상관계수 점수
- 2차 기준 : RandomForest 특징 중요도 
