import os
import cv2
import pandas as pd
import numpy as np
from collections import deque
from video_download import download
from ultralytics import YOLO

# YOLO 모델 로드
model = YOLO("analysis/yolo11n-seg.pt")

# CSV 파일 경로
csv_file = "Data\\GazeData\\iiIcTPoIoZk_2024-10-26-16-44-40.csv"
dt = "2024-10-26-16-44-40"

# CSV 데이터 로드
df = pd.read_csv(csv_file)

video_id = "iiIcTPoIoZk"

# 유튜브 영상 다운로드
video_only, audio_only, video_filename = download(video_id)

os.makedirs(f"Data/video/{video_id}/points", exist_ok=True)
point_video = f"Data/video/{video_id}/points/{video_id}_{dt}.mp4"

# 객체 이름과 색상 매핑
object_colors = {}
np.random.seed(0)  # 일관된 색상 분배

# 매칭된 객체 이름을 시간 순서대로 저장
object_sequence = []

# 비디오 열기
cap = cv2.VideoCapture(video_only)

# 비디오 속성 가져오기
fps = cap.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 비디오 너비
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 비디오 높이

# 비디오를 965x543 크기로 변환
output_width = 965
output_height = 543

# 비디오 출력 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(point_video, fourcc, fps, (output_width, output_height))

# 현재 프레임 인덱스
frame_idx = 0

# 점을 10초 동안 유지할 수 있도록 큐 설정
active_points = deque()

# 비디오를 프레임 단위로 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 현재 프레임에 해당하는 시간 계산 (초 단위)
    current_time = frame_idx / fps

    # 프레임 크기 조정
    frame_resized = cv2.resize(frame, (output_width, output_height))

    # YOLO 모델을 사용하여 객체 탐지 수행
    results = model(frame_resized)

    # 시선 좌표 값과 매칭된 객체 이름 저장
    matched_objects = set()
    for result in results:
        for obj in result.boxes:
            class_id = int(obj.cls)
            object_name = model.names[class_id]

            # 객체의 색상 설정 (같은 객체는 같은 색상)
            if object_name not in object_colors:
                object_colors[object_name] = tuple(np.random.randint(100, 255, 3).tolist())

            # 바운딩 박스 중심 좌표 계산
            xyxy = obj.xyxy.cpu().numpy()[0]  # 텐서를 넘파이 배열로 변환하여 좌표 추출
            x1, y1, x2, y2 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
            x = int((x1 + x2) / 2)
            y = int((y1 + y2) / 2)

            # CSV의 응시 데이터와 일치하는 객체를 찾음
            matching_rows = df[(df['Time'] >= current_time) & (df['Time'] < current_time + 0.1)]
            for _, row in matching_rows.iterrows():
                gaze_x, gaze_y = row['X'], row['Y']
                if not pd.isna(gaze_x) and not pd.isna(gaze_y):
                    # 객체가 시선 좌표와 매칭되었을 경우 이름을 저장
                    if x1 <= gaze_x <= x2 and y1 <= gaze_y <= y2:
                        matched_objects.add(object_name)

                    # 점을 큐에 추가 (10초 후에 제거)
                    color = object_colors[object_name] + (0.5,)  # 투명도 적용
                    active_points.append((gaze_x, gaze_y, current_time, color))

                    # 객체 이름을 시간 순서대로 저장 (중복된 연속 이름은 합침)
                    if not object_sequence or object_sequence[-1] != object_name:
                        object_sequence.append(object_name)

    # 10초 이상된 점 제거
    while active_points and current_time - active_points[0][2] > 5:
        active_points.popleft()

    # 활성 점을 그리기
    overlay = frame_resized.copy()
    for x, y, timestamp, color in active_points:
        color_bgr = (int(color[0]), int(color[1]), int(color[2]))
        cv2.circle(overlay, (int(x), int(y)), 10, color_bgr, -1)

    # 투명도를 적용하여 원본 프레임과 합성
    alpha = 0.5  # 투명도 설정
    frame_resized = cv2.addWeighted(overlay, alpha, frame_resized, 1 - alpha, 0)

    # 왼쪽 상단에 매칭된 객체 이름 표시
    y_offset = 20
    for obj_name in matched_objects:
        cv2.putText(frame_resized, obj_name, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        y_offset += 30

    # 비디오에 프레임 기록
    out.write(frame_resized)

    # 다음 프레임으로 이동
    frame_idx += 1

# 비디오와 출력 파일 닫기
cap.release()
out.release()

# 객체 이름 순서 출력
print(" -> ".join(object_sequence))

print(f"{point_video} 비디오 생성 완료")
