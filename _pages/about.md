---
title: "About"
layout: splash
permalink: /about/
author_profile: true
---

### 전현민 (Hyunmin Jeon)

<figure style="width:150px">
    <img src="{{ site.url }}{{ site.baseurl }}/assets/images/portfolio/profile.jpg" alt="">
</figure>

July 11, 1995

대한민국, 경상북도 포항시



## Skill

- Pytorch
- Tensorflow
- Python



## Interest

* Deep learning
* NLP
* Task-oriented dialogue system



## Education

M.S. in Computer Science & Engineering at POSTECH (2019.09 ~ 2021.08)

B.S. in Computer Science & Engineering at Hanyang University ERICA (2014.03 ~ 2019.08)



## Experience

* **POSTECH** / Researcher (2020.08 ~ 2020.12)

  국가 R&D 과제로 법률 챗봇 개발

* **POSTECH** / Teaching Assistant (2019.09 ~ 2019.12)

  컴퓨터 SW시스템 개론 (CSED211) 실습 조교

* **WiseNut** / Intern (2019.01 ~ 2019.02)

  산학 협력 캡스톤 디자인으로 머신러닝을 활용한 웹 크롤러 개발



## Research

* **DORA: Towards Policy Optimization for Task-oriented Dialogue System with Efficient Context**

  Submitted to Computer Speech & Language (Under review)

* **Domain State Tracking for a Simplified Dialogue System**

  arXiv preprint [[arXiv](https://arxiv.org/abs/2103.06648)]

* **Simplified Task-Oriented Dialogue System using Domain State**

  Workshop on AAAI 2021 (DSTC-9) [[Google Drive](https://drive.google.com/file/d/1UTFyFMTvW7P1UR79mX25FgserYaPc4Gd/view)]

* **도메인 상태를 이용한 다중 도메인 대화 상태 추적**

  제 32회 한글 및 한국어 정보처리 학술대회 (HCLT 2020) [[Google Drive](https://drive.google.com/file/d/1JpVnJ0cOxBEDys-TfPCNb5Wapvg4ZImW/view?usp=sharing)]

* **수기 답안지 자동 채점 시스템**

  한국정보과학회 학술발표논문집 2019 (KCC 2019) [[DBpia](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE08763608)]



## Project

### NLP

* **9th Dialog System Technology Challenge (DSTC-9)**

  대화 시스템 챌린지인 DSTC-9에 참여 [[DSTC-9 Workshop on AAAI 2021](https://sites.google.com/dstc.community/dstc9/aaai-21-workshop)]

  Microsoft가 주최한 *Multi-domain Task-oriented Dialog Challenge II* 트랙에 참여

  Multi-domain task-oriented dialogue system 개발 및 포스터 세션 발표 [[포스터](https://drive.google.com/file/d/18uRvgZtYzHQ-QA7jNrKhD4hBYn3brbcn/view?usp=sharing)]

* **법률 챗봇**

  국가 R&D 과제로 고소장 문서 자동 작성을 위한 법률 챗봇 개발

  GPT-2 기반의 belief tracker와 규칙 기반의 NLG를 결합

  SKT AI의 KoGPT-2를 법률 판례 데이터와 법률 상담 대화 데이터로 2차 pre-training 하여 LM으로 사용 [[KoGPT-2](https://github.com/SKT-AI/KoGPT2)] [[법률 판례 데이터](https://aihub.or.kr/aidata/29)] [[LM](https://github.com/gusalsdmlwlq/KoGPT2-LegalLM)]

  기업과 협업한 과제인 관계로 법률 상담 대화와 소스 코드는 비공개

  <details>
      <summary>프로토타입 데모 영상</summary>
      <figure class="align-center" style="width:600px">
      	<img src="{{ site.url }}{{ site.baseurl }}/assets/images/portfolio/legal_chatbot_demo.gif" alt="">
          <figcaption style="font-size:12px">프로토타입 데모 영상</figcaption>
      </figure>
  </details>

* **DS-DST belief tracker 논문 구현**

  Find or Classify? Dual Strategy for Slot-Value Predictions on Multi-Domain Dialog State Tracking (Zhang et al., 2019) [[논문](https://www.aclweb.org/anthology/2020.starsem-1.17/)]

  Pytorch 구현 [[Github](https://github.com/gusalsdmlwlq/DS-DST)]

* **KoGPT-2 summarization 모델**

  SKT AI의 KoGPT-2와 신문 기사 요약 데이터를 사용하여 summarization 모델 구현 [[신문 기사 요약 데이터](https://corpus.korean.go.kr/main.do#down)]

  Pytorch 구현 [[Github]()]

* **Machine translation 모델**

  Transformer와 ISWLT 2016 EN-DE 데이터를 사용하여 영어 $$\rightarrow$$ 독일어 translation 모델 구현 [[ISWLT 2016 데이터](https://wit3.fbk.eu/2016-01)]

  Attention is all you need (Vaswani et al., 2017) 논문 transformer 구현 [[논문](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)]

  Pytorch 구현 [[Github](https://github.com/gusalsdmlwlq/Machine-Translation)]

* **Sentiment analysis 모델**

  * Bidirectional LSTM과 Naver sentiment movie corpus (NSMC) 데이터를 사용하여 sentiment analysis 모델 구현 [[NSMC 데이터](https://github.com/e9t/nsmc)]

    Tensorflow 구현 [[Github](https://github.com/gusalsdmlwlq/Sentiment-Classification)]

  * 2019 오픈인프라 개발 경진대회에서 Youtube 댓글 분석 모델 구현

    Bidirectional LSTM과 NSMC & Sentiment 140 데이터를 사용하여 sentiment analysis 모델 구현 [[Sentiment 140 데이터](http://help.sentiment140.com/for-students)]

    Docker와 Tensorflow serving을 사용하여 모델 배포

    Tensorflow 구현 [[Github](https://github.com/open-tube/open-tube)]

### Etc

* **Worker model**

  Machine learning 대학원 수업 final project로 croudsourcing을 위한 worker model을 구현

  Belief propagation & Expectation maximization 알고리즘 사용

  Python 구현 [[Github](https://github.com/gusalsdmlwlq/WorkerModel)]

* **Machine learning 웹 크롤러**

  캡스톤 디자인으로 machine learning을 사용한 웹 크롤러 개발

  Scikit-learn의 SVM을 사용

  Puppeteer 라이브러리 사용

  Python & Node.js 구현 [[Github](https://github.com/gusalsdmlwlq/Crawler)]

* **지하철 빈 자리 체크 시스템**

  Global-PBL (in SIT, Japan) 프로그램 과제로 가상의 지하철의 빈 좌석 수를 체크하는 시스템 개발

  YOLO 알고리즘 사용

  Raspberry Pi와 Android 연동

  Python & Android 구현 [[Github](https://github.com/gusalsdmlwlq/RaspberryPi)]

* **모바일 리듬 게임**

  Unity3D를 사용하여 모바일 리듬 게임 어플리케이션 개발

  Unity3D & C# 구현 [[Github](https://github.com/gusalsdmlwlq/JeonHyunMin/tree/master/slimebeat)]

  <details>
      <summary>리듬 게임 영상</summary>
      <figure class="align-center" style="width:600px">
      	<img src="{{ site.url }}{{ site.baseurl }}/assets/images/portfolio/rhythm_game.gif" alt="">
          <figcaption style="font-size:12px">리듬 게임 영상</figcaption>
      </figure>
  </details>

* **웹 게시판**

  Raspberry Pi에 Raspbian OS를 설치하여 웹 서버로 사용

  APM & JS를 사용해 간단한 웹 게시판 기능 구현 [[Github](https://github.com/gusalsdmlwlq/JeonHyunMin/tree/master/pi)]



## Record

* **9th Dialog System Technology Challenge (DSTC-9)** / 2020.10.23

  Microsoft 주최의 *Multi-domain Task-oriented Dialog Challenge II* 트랙 참여 [[챌린지 사이트](https://sites.google.com/dstc.community/dstc9/aaai-21-workshop)]

  4위 (Team 6) [[리더보드](https://convlab.github.io/)]

* **Naver AI Hackathon 2019, speech recognition** / 2019.10.27

  네이버 주최 [[대회 사이트](https://campaign.naver.com/aihackathon_speech/)]

  결선 진출

  소스 코드 [[Github](https://github.com/gusalsdmlwlq/speech_hackathon_2019)]

* **2019 오픈인프라 개발 경진대회** / 2019.08.30

  (주) 맨텍 주최 [[대회 사이트](http://www.oidc.co.kr/oidc2019)]

  대상

  소스 코드 [[Github](https://github.com/open-tube/open-tube)]



## Certification

* **Global-PBL program in Shibaura Institute of Technology, Japan** / 2019.07.29

  [[Google Drive](https://drive.google.com/file/d/1lper0GH_ornzGGy9BgjTIiOXgM6y5Nj8/view?usp=sharing)]

* **Deep learning course from deeplearning.ai, Coursera** / 2019.06.24

  [[Google Drive](https://drive.google.com/file/d/173YGRDwsO_oOf9IuLhryDqVJlezVJgvc/view?usp=sharing)]

* **정보처리기사** / 2019.05.23

  [[Google Drive](https://drive.google.com/file/d/1IJ0MQsHdYUxLGWs0DJAuZazj03SUk2Jt/view?usp=sharing)]



## Contact

[gusalsrhkals@naver.com](mailto:gusalsrhkals@naver.com) / [jhm9507@postech.ac.kr](mailto:jhm9507@postech.ac.kr)

[LinkedIn](http://www.linkedin.com/in/jhm9507)

[Github](https://github.com/gusalsdmlwlq)