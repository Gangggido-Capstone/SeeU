import os
import subprocess
import cv2
import pandas as pd
from video_download import download

# CSV 파일 경로 
csv_file = "Data\GazeData\RoER-ab1QYw_2024-10-09-20-55-37.csv"
date_time = csv_file.split('_')[1].split('.')[0]

# CSV 데이터 로드
df = pd.read_csv(csv_file)

video_id = "RoER-ab1QYw"

# 유튜브 영상 다운로드
video_only, audio_only, video_filename = download(video_id)

os.makedirs(f"Data/video/{video_id}/points", exist_ok=True)
point_video = f"Data/video/{video_id}/points/{video_id}_{date_time}.mp4"

if not os.path.exists(point_video):
    cap = cv2.VideoCapture(video_only)

    # 비디오 속성 가져오기
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_width = 965
    output_height = 543

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_with_points = f"Data/video/{video_id}/points.mp4"
    out = cv2.VideoWriter(video_with_points, fourcc, fps, (output_width, output_height))

    frame_idx = 0
    previous_points = []  # 최근 5개의 좌표와 반지름 크기 저장
    point_counter = 1  # 숫자 카운터

    time_interval = 0.1
    frames_per_interval = int(time_interval * fps)

    def distance(p1, p2):
        """두 좌표 사이의 유클리드 거리 계산."""
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_idx / fps
        frame_resized = cv2.resize(frame, (output_width, output_height))

        # 현재 시간에 해당하는 좌표들 가져오기
        matching_rows = df[(df['Time'] >= current_time) & (df['Time'] < current_time + time_interval)]

        for _, row in matching_rows.iterrows():
            x, y = row['X'], row['Y']
            if not pd.isna(x) and not pd.isna(y):
                # 이전 좌표와 비교하여 거리가 50 이내인지 확인
                if previous_points and distance(previous_points[-1][:2], (x, y)) <= 50:
                    print("Time: "+ str(row['Time']) + ", " + "X: "+ str(int(x)) + ", " + "Y: "+ str(int(y)))
                    # 기존 좌표와 가까우면 반지름 증가
                    new_radius = previous_points[-1][2] + 1
                    previous_points[-1] = (int(x), int(y), new_radius)
                else:
                    # 새로운 위치일 경우 원 초기화 및 숫자 증가
                    new_radius = 15  # 기본 반지름 크기
                    previous_points.append((int(x), int(y), new_radius))
                    point_counter += 1

                # 최대 5개 좌표만 유지
                if len(previous_points) > 5:
                    previous_points.pop(0)

        # 모든 좌표에 대해 원과 선 그리기
        for i in range(len(previous_points)):
            x, y, radius = previous_points[i]
            cv2.circle(frame_resized, (x, y), radius, (0, 255, 0), -1)

            # 새 좌표에는 숫자 표시, 이전 좌표에는 숫자 없음
            if i == len(previous_points) - 1:
                cv2.putText(frame_resized, str(point_counter), (x - 5, y + 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            # 이전 좌표와 선으로 연결 (첫 번째 점은 제외)
            if i > 0:
                prev_x, prev_y, _ = previous_points[i - 1]
                cv2.line(frame_resized, (prev_x, prev_y), (x, y), (255, 0, 0), 2)

        out.write(frame_resized)
        frame_idx += 1

    cap.release()
    out.release()

    merge_command = [
        'ffmpeg',
        '-i', video_with_points,
        '-i', audio_only,
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-r', '30',
        '-vsync', 'cfr',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        point_video
    ]

    subprocess.run(merge_command)

    if os.path.exists(video_with_points):
        os.remove(video_with_points)
        print(f"{video_with_points} 파일이 삭제되었습니다.")

    print(f"{point_video} 비디오 생성 완료")

else:
    print(f"{point_video} 이미 존재합니다.")
