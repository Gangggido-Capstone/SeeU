from video_download import download
from concurrent.futures import ThreadPoolExecutor
from sklearn.cluster import DBSCAN
from collections import Counter
from ultralytics import YOLO
import numpy as np
import pandas as pd
import time
import cv2
import os

# YOLO 모델
yolo_model = YOLO("analysis/yolo11n.pt")

def detectObjects(frame):
    results = yolo_model(frame)
    detected_object = []

    # 결과에서 각 객체 정보 추출
    for res in results:
        for obj in res.boxes:
            class_id = int(obj.cls)  # 객체의 클래스 ID
            confidence = obj.conf    # 신뢰도
            if confidence > 0.8:     # 신뢰도가 0.8 이상인 경우만 추가
                detected_object.append(yolo_model.names[class_id])  # 객체 이름 추가
    
    return detected_object

def gazeVisualization(video_id, video_csv, video_only, video_width, video_height):
    date_time = video_csv.split('_')[1].split('.')[0]  # 파일명에서 날짜 추출
    gaze_csv = pd.read_csv(video_csv)  # CSV 파일 로드
    gaze_csv = gaze_csv.dropna(subset=['Time', 'X', 'Y'])  # Null 값을 가지는 좌표 제거

    # 비디오 열기
    cap = cv2.VideoCapture(video_only)
    video_path = f'Data/video/{video_id}/point_test/{video_id}_{date_time}.mp4'
    os.makedirs(os.path.dirname(video_path), exist_ok=True)  # 필요한 폴더가 없으면 생성

    # 비디오 속성 설정
    fps = cap.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수 가져오기
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 비디오 코덱 설정
    out = cv2.VideoWriter(video_path, fourcc, fps, (video_width, video_height))  # 비디오 파일 쓰기 설정

    # DBSCAN 알고리즘을 사용해 클러스터링 수행
    dbscan = DBSCAN(eps=27, min_samples=5)
    coords = gaze_csv[['X', 'Y']].values
    clustering = dbscan.fit(coords)
    gaze_csv['Cluster'] = clustering.labels_  # 클러스터 라벨 추가

    # 색상 설정
    green_color = (0, 255, 0, 128)  # 초록색 (클러스터)
    red_color = (0, 0, 255, 128)    # 빨간색 (잡음)

    # 클러스터 색상 설정: 클러스터가 -1이 아니면 초록색, 아니면 빨간색
    colors = {
        label: green_color if label != -1 else red_color
        for label in np.unique(clustering.labels_)
    }

    points = []  # 화면에 그릴 점 정보 저장
    objects = []  # 감지된 객체 이름 저장

    point_radius = 7  # 점의 반지름 설정

    # 병렬 처리를 위해 ThreadPoolExecutor 사용
    with ThreadPoolExecutor(max_workers=4) as executor:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (video_width, video_height))  # 프레임 크기 조정
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # 현재 시간 계산

            # 객체 탐지를 병렬로 수행
            future_detect = executor.submit(detectObjects, frame)
            detected_objects = future_detect.result()

            frame_objects = set()  # 현재 프레임의 객체 이름 저장
            frame_points = gaze_csv[(gaze_csv['Time'] >= current_time - 1 / fps) & (gaze_csv['Time'] < current_time)]

            overlay = frame.copy()  # 점 그리기를 위한 오버레이 생성

            new_points = []
            for x, y, t, color in points:
                if current_time - t <= 1.5:  # 1.5초 이상 지난 점은 제거
                    cv2.circle(overlay, (x, y), point_radius, color[:3], -1)
                    new_points.append((x, y, t, color))

            for _, gaze in frame_points.iterrows():
                x, y = int(gaze['X']), int(gaze['Y'])
                cluster_id = gaze['Cluster']
                color = colors.get(cluster_id, (192, 192, 192, 128))
                cv2.circle(overlay, (x, y), point_radius, color[:3], -1)
                new_points.append((x, y, current_time, color))

                for obj in detected_objects:
                    if obj not in frame_objects:
                        frame_objects.add(obj)

            # 오버레이와 원본 프레임을 합침
            alpha = 0.4
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # 객체 이름을 프레임에 표시
            for i, obj in enumerate(frame_objects):
                cv2.putText(frame, obj, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # 중복되지 않도록 객체 이름을 추가
            if frame_objects:
                for obj in frame_objects:
                    if obj not in objects or obj != objects[-1]:
                        objects.append(obj)

            points = new_points
            out.write(frame)  # 처리된 프레임을 비디오에 저장

    # 객체 빈도수 저장
    object_freq = Counter(objects)
    total_objects = len(objects)
    object_freq = {obj: (count / total_objects) * 100 for obj, count in object_freq.items()}

    # 객체 탐지 순서 저장
    object_order = []
    for obj in objects:
        if not object_order or object_order[-1] != obj:
            object_order.append(obj)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return video_path, object_freq, object_order

if __name__ == "__main__":
    start = time.time()

    video_id = "iiIcTPoIoZk"
    video_csv = "Data/GazeData/iiIcTPoIoZk_2024-10-26-16-44-40.csv"
    video_width, video_height = 965, 543

    video_only = download(video_id)

    video_point, object_freq, object_order = gazeVisualization(video_id, video_csv, video_only, video_width, video_height)
    print(video_point)
    print()
    print(object_freq)
    print()
    print(object_order)
    print()
    point_end = time.time()
    print(f"point end: {point_end - start:.5f} sec")
