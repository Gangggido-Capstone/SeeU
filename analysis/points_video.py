import os
import subprocess
import cv2
import pandas as pd
from video_download import download

# CSV 파일 경로
csv_file = "Data\\GazeData\\0gkPFSvVvFw_2024-10-12-18-56-44.csv"
dt = "2024-10-12-18-56-44"

# CSV 데이터 로드
df = pd.read_csv(csv_file)

video_id = "0gkPFSvVvFw"

# 유튜브 영상 다운로드
video_only, audio_only, video_filename = download(video_id)

os.makedirs(f"Data/video/{video_id}/points", exist_ok=True)
point_video = f"Data/video/{video_id}/points/{video_id}_{dt}.mp4"

if not os.path.exists(point_video):
    # 비디오 열기
    cap = cv2.VideoCapture(video_only)

    # 비디오 속성 가져오기
    fps = cap.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 비디오 너비
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 비디오 높이
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 총 프레임 수

    # 비디오를 1207x679 크기로 변환 (노트북: 965X543)
    output_width = 965
    output_height = 543

    # 비디오 출력 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_with_points = f"Data/video/{video_id}/points.mp4"
    out = cv2.VideoWriter(video_with_points, fourcc, fps, (output_width, output_height))


    # 현재 프레임 인덱스
    frame_idx = 0

    # Time 간격을 프레임 수로 변환 (0.1초 간격)
    time_interval = 0.1
    frames_per_interval = int(time_interval * fps)

    # 비디오를 프레임 단위로 처리
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 현재 프레임에 해당하는 시간 계산 (초 단위)
        current_time = frame_idx / fps
        
        # 프레임 크기 조정
        frame_resized = cv2.resize(frame, (output_width, output_height))
        
        # Time 값에 해당하는 데이터 가져오기
        matching_rows = df[(df['Time'] >= current_time) & (df['Time'] < current_time + time_interval)]
        
        # 각 행에 대해 X, Y 좌표에 점 그리기 (null 값 무시)
        for _, row in matching_rows.iterrows():
            x, y = row['X'], row['Y']
            if not pd.isna(x) and not pd.isna(y):
                # X, Y 좌표에 점 그리기 (파란색 점, 반지름 5)
                print("Time: "+ str(row['Time']) + ", " + "X: "+ str(int(x)) + ", " + "Y: "+ str(int(y)))
                cv2.circle(frame_resized, (int(x), int(y)), 5, (250, 0, 0), -1)
        
        # 결과 프레임을 비디오에 기록
        out.write(frame_resized)
        
        # 다음 프레임으로 이동
        frame_idx += 1

    # 비디오와 출력 파일 닫기
    cap.release()
    out.release()

    #  ==========================================================  #

    # ffmpeg를 사용해 비디오와 오디오 병합
    merge_command = [
        'ffmpeg',
        '-i', video_with_points,         # 좌표가 그려진 비디오 파일
        '-i', audio_only,         # 입력 오디오 파일
        '-c:v', 'libx264',        # 비디오를 H.264로 재인코딩
        '-preset', 'fast',        # 빠른 인코딩 옵션
        '-c:a', 'aac',            # 오디오를 AAC 형식으로 변환
        '-b:a', '192k',           # 오디오 비트레이트 설정
        '-r', '30',               # 비디오 프레임 속도 강제 설정 (30fps, 고정 프레임 속도)
        '-vsync', 'cfr',          # 고정 프레임 속도 동기화
        '-map', '0:v:0',          # 비디오 스트림을 첫 번째 입력에서 가져오기
        '-map', '1:a:0',          # 오디오 스트림을 두 번째 입력에서 가져오기
        '-shortest',              # 가장 짧은 스트림 기준으로 맞추기
        point_video                 # 최종 출력 파일 경로
    ]

    # 병합 명령어 실행
    subprocess.run(merge_command)

    # 병합 완료 후 비디오 및 오디오 파일 삭제
    if os.path.exists(video_with_points):
        os.remove(video_with_points)
        print(f"{video_with_points} 파일이 삭제되었습니다.")

    print(f"{point_video} 비디오 생성 완료")

else:
        print(f"{point_video} 이미 존재합니다.")