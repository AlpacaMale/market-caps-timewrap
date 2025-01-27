from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import cv2
import os
from config import DATA_PATH, IMG_PATH, VIDEO_PATH


def draw_img():
    market_caps_df = pd.read_scv(f"./{DATA_PATH}/mktcp_data.csv")
    matplotlib.rcParams["font.family"] = "Malgun Gothic"
    colors = plt.cm.get_cmap("tab20", len(market_caps_df.index))(
        range(len(market_caps_df.index))
    )
    for index in tqdm(range(1, len(market_caps_df.columns))):
        if index % 3 == 0:
            plt.figure(figsize=(18, 12))
            for color, title in zip(colors, market_caps_df.index):
                x = market_caps_df.loc[title].index[:index]
                y = market_caps_df.loc[title].values[:index]
                if y[-1] < 1:
                    continue
                plt.plot(x, y, color=color)
                plt.scatter(x[-1], y[-1], color=color)
                plt.text(x[-1], y[-1], title, ha="left", va="center", color=color)
            plt.xticks([])
            plt.yticks([])
            plt.title(x[-1][:7], fontsize=32, weight="bold")
            plt.savefig(f".{IMG_PATH}/{index}.png", dpi=300)


def convert_mp4():
    video_name = "mktcp_timewrap.mp4"
    # 이미지 파일 목록 가져오기
    images = [img for img in os.listdir(IMG_PATH) if img.endswith(".png")]
    images.sort(key=extract_number)

    # 첫 번째 이미지로부터 프레임 크기 가져오기
    frame = cv2.imread(os.path.join(IMG_PATH, images[0]))
    height, width, layers = frame.shape

    # 비디오 코덱 설정 (MP4 파일을 생성하기 위해 'mp4v 사용)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # 비디오 작성기 생성 (초당 24프레임으로 설정)
    video = cv2.VideoWriter(f"{VIDEO_PATH}/{video_name}", fourcc, 23, (width, height))

    for image in tqdm(images):
        img_path = os.path.join(IMG_PATH, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()


def extract_number(filename):
    # 파일 이름에서 숫자 부분만 추출
    numbers = filename.split(".")
    return int(numbers[0])
