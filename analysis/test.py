from video_download import download
from sklearn.cluster import DBSCAN
from collections import Counter
from ultralytics import YOLO
import numpy as np
import pandas as pd
import cv2

# YOLOv11 모델 로드
yolo_model = YOLO("analysis/yolo11n.pt")

# DBSCAN 파라미터 설정
dbscan = DBSCAN(eps=27, min_samples=5)

def detect_objects(frame):
    # YOLOv11 모델로 객체 탐지 수행
    results = yolo_model(frame)
    detected_objects = []

    for result in results:
        for obj in result.boxes:
            class_id = int(obj.cls)
            confidence = obj.conf
            if confidence > 0.8:  # 신뢰도 기준 설정
                detected_objects.append(yolo_model.names[class_id])
    
    return detected_objects

def process_video(video_id, video_csv, video_only):

    # 시드 설정
    np.random.seed(42)

    date_time = video_csv.split('_')[1].split('.')[0]
    gaze_csv = pd.read_csv(video_csv)    

    # Null 값이 있는 좌표는 그리기 시점에 검사하고 건너뛴다
    gaze_csv = gaze_csv.dropna(subset=['Time', 'X', 'Y'])

    # 비디오 열기
    cap = cv2.VideoCapture(video_only)
    video_path = f'Data/video/{video_id}/point_test/{video_id}_{date_time}.mp4'
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_width, video_height = 965, 543
    
    out = cv2.VideoWriter(video_path, fourcc, fps, (video_width, video_height))

    # 클러스터링 수행
    coords = gaze_csv[['X', 'Y']].values
    clustering = dbscan.fit(coords)
    gaze_csv['Cluster'] = clustering.labels_

    # 색상 설정: 초록색(클러스터)과 빨간색(노이즈) 설정
    colors = {
        label: (0, 255, 0, 128) if label != -1 else (0, 0, 255, 128)  # 클러스터: 초록색, 노이즈: 빨간색
        for label in np.unique(clustering.labels_)
    }

    detected_objects_list = []
    displayed_points = []
    displayed_object_names = []

    point_radius = 7  # 점의 반지름 크기 설정

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 크기 조정
        frame = cv2.resize(frame, (video_width, video_height))

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        detected_objects = detect_objects(frame)
        detected_objects_list.extend(detected_objects)

        # 현재 프레임에서 감지된 객체와 좌표가 일치하는 객체의 이름을 저장
        frame_object_names = set()

        # 현재 시간에 해당하는 응시 데이터 필터링
        frame_gaze_points = gaze_csv[(gaze_csv['Time'] >= current_time - 1 / cap.get(cv2.CAP_PROP_FPS)) & (gaze_csv['Time'] < current_time)]

        for _, gaze in frame_gaze_points.iterrows():
            x, y = int(gaze['X']), int(gaze['Y'])
            cluster_id = gaze['Cluster']

            # 클러스터 색상 설정
            color = colors.get(cluster_id, (192, 192, 192, 128))

            # 점에 투명도를 적용하기 위해 알파 채널 사용
            overlay = frame.copy()
            cv2.circle(overlay, (x, y), point_radius, color[:3], -1)
            alpha = color[3] / 255.0
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # 감지된 객체 영역과 일치하는 경우
            for obj_name in detected_objects:
                if obj_name not in frame_object_names:
                    frame_object_names.add(obj_name)

            # 점 기록
            displayed_points.append((x, y, current_time, color))

        # 왼쪽 상단에 감지된 객체 이름 표시
        for i, obj_name in enumerate(frame_object_names):
            cv2.putText(frame, obj_name, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 객체 이름을 중복되지 않도록 순서대로 추가
        if frame_object_names:
            for obj_name in frame_object_names:
                if obj_name not in displayed_object_names or obj_name != displayed_object_names[-1]:
                    displayed_object_names.append(obj_name)

        # 오래된 점 제거 (3초)
        displayed_points = [(x, y, t, c) for x, y, t, c in displayed_points if current_time - t <= 3]
        for x, y, _, color in displayed_points:
            overlay = frame.copy()
            cv2.circle(overlay, (x, y), point_radius, color[:3], -1)
            alpha = color[3] / 255.0
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        out.write(frame)

    # 객체 빈도수 및 순서 출력
    print("\n좌표 영역에 있던 객체 빈도수:")
    object_freq = Counter(displayed_object_names)
    for obj, count in object_freq.most_common():
        print(f"{obj}: {count}회 ({count / len(displayed_object_names) * 100:.2f}%)")

    print("\n객체 감지 순서:")
    unique_sequence = []
    for obj in displayed_object_names:
        if not unique_sequence or unique_sequence[-1] != obj:
            unique_sequence.append(obj)
    print(" -> ".join(unique_sequence))

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_id = "iiIcTPoIoZk"
    video_csv = "Data/GazeData/iiIcTPoIoZk_2024-10-26-16-44-40.csv"
    video_only = download(video_id)
    process_video(video_id, video_csv, video_only)