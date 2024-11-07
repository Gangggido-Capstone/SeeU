from video_download import download
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import time
import cv2
import os

def get_root_path():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(root_dir, 'README.md')):
        root_dir = os.path.abspath(os.path.join(root_dir, '..'))
    current_dir = os.path.join(root_dir, "frontend", "public")
    return current_dir

def gazeVisualization(video_id, video_csv, video_only, video_width, video_height):
    root_path = get_root_path()
    date_time = video_csv.split('_')[1].split('.')[0]  # 파일명에서 날짜 추출

    csv_path = os.path.join(root_path, "data", "GazeData")
    gaze_csv = pd.read_csv(os.path.join(csv_path, video_csv))
    gaze_csv = gaze_csv.dropna(subset=['Time', 'X', 'Y'])

    print("gaze data: " + str(len(gaze_csv[['X', 'Y']].values)))
    if(len(gaze_csv[['X', 'Y']].values) <= 10):
        v = f"{video_id}\\{video_id}.mp4"
        return v
    
    else:
        points_dir = os.path.join(root_path, "data", "video", video_id, "points")
        os.makedirs(points_dir, exist_ok=True)
        
        video_point = os.path.join(points_dir, f"{video_id}_{date_time}.mp4")

        # 비디오 열기
        cap = cv2.VideoCapture(video_only)

        # 비디오 속성 설정
        fps = cap.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수 가져오기
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 비디오 코덱 설정
        out = cv2.VideoWriter(video_point, fourcc, fps, (video_width, video_height))  # 비디오 파일 쓰기 설정

        # DBSCAN 알고리즘을 사용해 클러스터링 수행
        dbscan = DBSCAN(eps=27, min_samples=5)
        coords = gaze_csv[['X', 'Y']].values
        clustering = dbscan.fit(coords)
        gaze_csv['Cluster'] = clustering.labels_

        # 색상 설정
        green_color = (0, 255, 0, 128)  # 초록색 (클러스터)
        red_color = (0, 0, 255, 128)    # 빨간색 (잡음)

        colors = {
            label: green_color if label != -1 else red_color
            for label in np.unique(clustering.labels_)
        }

        points = []  # 화면에 그릴 점 정보 저장
        point_radius = 7  # 점의 반지름 설정

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (video_width, video_height))  # 프레임 크기 조정
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # 현재 시간 계산
            frame_points = gaze_csv[(gaze_csv['Time'] >= current_time - 1 / fps) & (gaze_csv['Time'] < current_time)]

            overlay = frame.copy()  # 점 그리기를 위한 오버레이 생성

            new_points = []
            for x, y, t, color in points:
                if current_time - t <= 1.5:  # 1.5초 이상 지난 점은 제거
                    cv2.circle(overlay, (x, y), point_radius, color[:3], -1)
                    new_points.append((x, y, t, color))

            for _, gaze in frame_points.iterrows():
                x, y = gaze['X'], gaze['Y']
                if not pd.isna(x) and not pd.isna(y):
                    x, y = int(x), int(y)
                    cluster_id = gaze['Cluster']
                    color = colors[cluster_id]
                    cv2.circle(overlay, (x, y), point_radius, color[:3], -1)
                    new_points.append((x, y, current_time, color))

            # 오버레이와 원본 프레임을 합침
            alpha = 0.4
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            points = new_points
            out.write(frame)  # 처리된 프레임을 비디오에 저장

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        point_video = f"{video_id}\\points\\{video_id}_{date_time}.mp4"
        return point_video

if __name__ == "__main__":
    start = time.time()

    video_id = ""
    video_csv = ""
    video_width, video_height = 965, 543

    video_only = download(video_id)

    video_point = gazeVisualization(video_id, video_csv, video_only, video_width, video_height)
    print(video_point)

    point_end = time.time()
    print(f"point end: {point_end - start:.5f} sec")