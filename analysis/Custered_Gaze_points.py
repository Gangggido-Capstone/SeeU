import os
import cv2
import pandas as pd
import numpy as np
from collections import defaultdict, deque
from sklearn.cluster import DBSCAN
from ultralytics import YOLO

model = YOLO("analysis/yolo11n-seg.pt")

# 설정 변수
video_id = "0gkPFSvVvFw"
video_csv = "Data/GazeData/0gkPFSvVvFw_2024-10-12-18-56-44.csv"
date_time = video_csv.split('_')[1].split('.')[0]
input_video_path = f'Data/video/{video_id}/{video_id}.mp4'
video_path = f'Data/video/{video_id}/clustered/{video_id}_{date_time}.mp4'

# 디렉토리 생성
output_dir = os.path.dirname(video_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 응시 데이터 로드
gaze_data = pd.read_csv(video_csv)
gaze_data = gaze_data.dropna(subset=['X', 'Y'])
coordinates = gaze_data[['X', 'Y']].values

# DBSCAN 클러스터링 및 색상 설정
dbscan = DBSCAN(eps=15, min_samples=5)
gaze_data['Cluster'] = dbscan.fit_predict(coordinates)
gaze_data = gaze_data[gaze_data['Cluster'] != -1]

# 클러스터마다 고유 색상 설정
used_colors = set()
def generate_unique_color():
    while True:
        color = tuple(np.random.randint(0, 255, 3).tolist())
        if color not in used_colors:
            used_colors.add(color)
            return color
cluster_colors = {cluster_id: generate_unique_color() for cluster_id in gaze_data['Cluster'].unique()}

# 각 시간에 매칭된 객체 이름을 기록할 리스트
object_sequence = []

# 비디오 로드
cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
video_width, video_height = 965, 543
out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (video_width, video_height))

# 이전 객체 이름을 기억하여 중복 방지
last_object_name = None

# 비디오 프레임 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (video_width, video_height))
    
    # 현재 비디오 재생 시간
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    
    # YOLO 객체 탐지
    results = model(frame, task='detection')
    frame_object_names = set()  # 현재 프레임에서 탐지된 객체 이름 저장

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_name = str(result.names[int(box.cls[0])])  # 객체 이름

            # 객체 이름만 표시
            cv2.putText(frame, cls_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # 객체 영역에 gaze 데이터가 있는 경우 객체 이름 매칭
            gaze_points_in_box = gaze_data[(gaze_data['X'] >= x1) & (gaze_data['X'] <= x2) &
                                           (gaze_data['Y'] >= y1) & (gaze_data['Y'] <= y2) &
                                           (gaze_data['Time'] >= current_time - 1/fps) & 
                                           (gaze_data['Time'] < current_time)]
            if not gaze_points_in_box.empty:
                frame_object_names.add(cls_name)  # 객체 이름 추가
    
    # 중복되지 않도록 순서대로 객체 이름 나열
    for name in frame_object_names:
        if name != last_object_name:
            object_sequence.append(name)
            last_object_name = name
    
    # 응시 데이터 추가
    frame_gaze_points = gaze_data[(gaze_data['Time'] >= current_time - 1/fps) & (gaze_data['Time'] < current_time)]
    for _, gaze in frame_gaze_points.iterrows():
        x, y = int(gaze['X']), int(gaze['Y'])
        cluster_id = gaze['Cluster']
        
        # 클러스터 색상 설정
        if cluster_id not in cluster_colors:
            cluster_colors[cluster_id] = generate_unique_color()
        
        color = cluster_colors[cluster_id]
        cv2.circle(frame, (x, y), 8, color, -1)
    
    out.write(frame)

# 자원 해제
cap.release()
out.release()
print(f"비디오 저장 완료: {video_path}")

# 최종 객체 이름 시퀀스 출력
print("객체 시퀀스:", " -> ".join(object_sequence))
