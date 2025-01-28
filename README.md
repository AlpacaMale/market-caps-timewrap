# Korean Market Capitalization Rank History Time Wrap

## 개요

과거 한국 기업중 한 번이라도 시가총액이 상위 10위 안에 랭크된 주식들의 시가총액을 시각화하여 타임랩스로 기록한다.

## 목차

- [To-Do List](#to-do-list)
- [패키지 구조](#패키지-구조)
- [사용 모듈](#사용-모듈)
- [실행 방법](#실행-방법)
- [실행 영상](#실행-영상)

## To-Do List

- [x] **scrape top 10 companies**: 과거 한 번이라도 상위 10에 랭크된 적이 있는 기업의 목록을 구한다.
- [x] **convert top 10 list to csv**: 기업의 리스트를 파일 형태로 저장한다.
- [x] **scrape listing date**: 기업의 상장일을 알아낸다. 어느 일자로부터 주식 데이터를 스크래핑해야되는지 알 수 있다.
- [x] **convert listing date to csv**: 상장일을 파일 형태로 저장한다.
- [x] **scrape histroy data**: 기업의 상장일로부터 오늘날까지 시가총액 데이터를 하루단위로 구한다.
- [x] **convert history data to csv**: 과거 시가총액 데이터를 파일 형태로 저장한다.
- [x] **draw & save images**: matplotlib를 이용해서 그래프를 그리고 png로 저장한다.
- [x] **refactor scraper code**: 스크래핑 코드 함수화, 모듈화
- [x] **refactor matplotlib code**: 데이터 시각화 코드 함수화, 모듈화
- [x] **convert to mp4**: 이미지들을 mp4 파일로 변환한다.
- [x] **comment out**: 주석 달기
- [ ] **set yticks**: 시가총액이 한화로 얼마인지 시각적으로 나타내주기
- [ ] **fix fill na method**: 결측값을 0으로 하지 않고 구현할 방법 연구 그래프가 고장나지 않기 위함
- [ ] **insert bgm**: 영상에 맞는 적절한 bgm을 넣는다.
- [ ] **handle exception**: 예외 처리

## 패키지 구조

```
├── 📁 data / directory for csv files
├── 📁 img / directory for image files
├── 📁 video / directory for video files
├── note.ipynb / program logics
├── main.py / main entry for python program
├── crawler.py / crawling logics
├── timewrap.py / create the visualized images and convert it mp4 format
├── config.py / configure settings
├── requirements.txt / package dependency
└── README.md
```

## 사용 모듈

- **Requests**: HTTP 요청을 간편하게 보내고 응답을 처리해준다.
- **Pandas**: 데이터를 읽고, 쓰고, 가공하는 다양한 기능을 처리한다.
- **Time**: sleep 함수를 사용하여 프로그램에 딜레이를 준다.
- **Pandas**: 데이터를 읽고, 쓰고, 가공하는 다양한 기능을 처리한다.
- **Datetime**: 날짜, 시간에 대한 연산 기능을 제공하고, 시간과 시간 형태의 문자열 변환 작업을 한다.
- **Relativedelta**: Datetime 모듈에서 제공하지 않는 1년 단위의 시간 연산을 제공한다.
- **Tqdm**: 반복문의 진행 정도를 콘솔에 나타낸다.
- **matplotlib**: 데이터 시각화 관련 기능을 제공한다.

## 실행 방법

1. **Clone repository**

```
git clone https://github.com/AlpacaMale/market-caps-timewrap
```

2. **Change directory**

```
cd market-caps-timewrap
```

3. **Install dependency**

```
pip install -r requirements.txt
```

4. **Run main.py**

```
python main.py
```

## 실행 영상

[유투브](https://youtu.be/6wAmTDixp6E)
