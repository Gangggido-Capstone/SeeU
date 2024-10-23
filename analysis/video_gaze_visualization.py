import os
import subprocess
import cv2
import pandas as pd
import numpy as np
from scipy.interpolate import splprep, splev
from video_download import download

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_dir, 'README.md')):
        current_dir = os.path.abspath(os.path.join(current_dir, '..'))
    return current_dir

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def draw_circle(image, center, radius, color, alpha=1.0):
    overlay = image.copy()
    cv2.circle(overlay, center, radius, color, -1)
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def gazeVisualization(video_id, video_csv, video_only, audio_only):
    # 프로젝트 루트 경로 설정
    root_path = get_root_path()
    
    # 날짜 시간 값
    date_time = video_csv.split('_')[1].split('.')[0]

    # CSV 파일 불러오기
    csv_path = os.path.join(root_path, "Data", "GazeData")
    gaze_csv = pd.read_csv(os.path.join(csv_path, video_csv))

    points_dir = os.path.join(root_path, "Data", "video", video_id, "points")
    os.makedirs(points_dir, exist_ok=True)

    video_point = os.path.join(points_dir, f"{video_id}_{date_time}.mp4")
    if not os.path.exists(video_point):
        video_capture = cv2.VideoCapture(video_only)

        # 비디오 속성 가져오기
        fps = video_capture.get(cv2.CAP_PROP_FPS)

        video_width = 965
        video_height = 543

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_temp = os.path.join(root_path, "Data", "video", video_id, "points.mp4")
        video_writer = cv2.VideoWriter(video_temp, fourcc, fps, (video_width, video_height))

        frame_idx = 0
        previous_points = []  # 최근 5개의 좌표와 반지름 크기 저장

        time_interval = 0.2  # 원이 생성되는 시간 간격 조정

        # 색상 그라데이션과 투명도를 위한 값 설정
        max_alpha = 1.0
        min_alpha = 0.35

        # 색상 설정 (BGR 형식)
        circle_color = (152, 255, 152)  # 밝은 민트
        line_color = (0, 0, 0)  # 블랙 
        text_color = (0, 0, 0)  # 블랙

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break

            current_time = frame_idx / fps
            current_time_int = int(current_time)  # 현재 시간 값을 정수로 변환하여 표시
            frame_resized = cv2.resize(frame, (video_width, video_height))

            # 현재 시간에 해당하는 좌표들 가져오기
            matching_rows = gaze_csv[(gaze_csv['Time'] >= current_time) & (gaze_csv['Time'] < current_time + time_interval)]

            for _, row in matching_rows.iterrows():
                x, y = row['X'], row['Y']
                if not pd.isna(x) and not pd.isna(y):
                    # 이전 좌표와 비교하여 거리가 50 이내인지 확인
                    if previous_points and distance(previous_points[-1][:2], (x, y)) <= 50:
                        # print("Time: "+ str(row['Time']) + ", " + "X: "+ str(int(x)) + ", " + "Y: "+ str(int(y)))
                        
                        # 기존 좌표와 가까우면 반지름 증가
                        new_radius = previous_points[-1][2] + 1
                        previous_points[-1] = (int(x), int(y), new_radius)
                    else:
                        # 새로운 위치일 경우 원 초기화 및 숫자 증가
                        new_radius = 15  # 기본 반지름 크기
                        previous_points.append((int(x), int(y), new_radius))

                    # 최대 5개 좌표만 유지
                    if len(previous_points) > 5:
                        previous_points.pop(0)

            # 스플라인 보간법을 사용한 부드러운 곡선 그리기 (좌표가 4개 이상일 때만)
            if len(previous_points) >= 4:
                try:
                    x_coords = [p[0] for p in previous_points]
                    y_coords = [p[1] for p in previous_points]

                    # splprep 함수는 최소 4개의 좌표가 필요합니다.
                    if len(x_coords) >= 4 and len(y_coords) >= 4:
                        tck, u = splprep([x_coords, y_coords], s=0)
                        unew = np.linspace(0, 1, 100)
                        out = splev(unew, tck)

                        for i in range(1, len(out[0])):
                            pt1 = (int(out[0][i - 1]), int(out[1][i - 1]))
                            pt2 = (int(out[0][i]), int(out[1][i]))
                            alpha = max_alpha - (max_alpha - min_alpha) * (i / len(out[0]))
                            color = line_color
                            cv2.line(frame_resized, pt1, pt2, color, 2)
                except ValueError as e:
                    # print(f"Splprep Error: {e}")
                    # If splprep fails, fall back to direct line drawing between points
                    for i in range(1, len(previous_points)):
                        pt1 = (previous_points[i - 1][0], previous_points[i - 1][1])
                        pt2 = (previous_points[i][0], previous_points[i][1])
                        cv2.line(frame_resized, pt1, pt2, line_color, 2)
            else:
                # 좌표가 3개 이하일 때는 직선 연결
                for i in range(1, len(previous_points)):
                    pt1 = (previous_points[i - 1][0], previous_points[i - 1][1])
                    pt2 = (previous_points[i][0], previous_points[i][1])
                    cv2.line(frame_resized, pt1, pt2, line_color, 2)

            # 모든 좌표에 대해 원을 그리고 투명도 적용 (가장 최근 좌표가 불투명)
            for i in range(len(previous_points)):
                x, y, radius = previous_points[i]
                alpha = min_alpha + (i / len(previous_points)) * (max_alpha - min_alpha)  # 최근 값일수록 투명도가 낮아지도록 수정
                frame_resized = draw_circle(frame_resized, (x, y), radius, circle_color, alpha)

                # 원 중앙에 해당 정수 시간 값을 표시
                if i == len(previous_points) - 1:
                    cv2.putText(frame_resized, str(current_time_int), (int(x) - 10, int(y) + 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)  # 원 중앙에 시간 표시

            video_writer.write(frame_resized)
            frame_idx += 1

        video_capture.release()
        video_writer.release()

        try:
            ffmpeg_path = "C:/ffmpeg/bin/ffmpeg" 
            merge_command = [
                ffmpeg_path,
                '-i', video_temp,
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
                video_point
            ]
            print("subprocess.run")
            subprocess.run(merge_command, timeout = 800)
            print(f"{video_temp} 다운 완료")
        except subprocess.TimeoutExpired:
            print("FFmpeg 실행이 타임아웃되었습니다.")

        if os.path.exists(video_temp):
            os.remove(video_temp)
            print(f"{video_temp} temp 파일 삭제")

        print(f"{video_point} 비디오 생성 완료")

    else:
        print(f"{video_point} 이미 존재합니다.")

    return video_point


if __name__ == "__main__":
    
    # video_id, video_csv는 스프링에서 넘겨야 함
    # UrEHWclh7Co 삼성카드
    # 0gkPFSvVvFw 전란
    # fRaIcUhaXXQ 핫초코
    # video_id = "0gkPFSvVvFw"
    # video_csv = "0gkPFSvVvFw_2024-10-12-18-56-44.csv"
    video_id = "fRaIcUhaXXQ"
    video_csv = "fRaIcUhaXXQ_2024-10-20-16-50-56.csv"

    # 영상 다운
    video_only, audio_only, video_filename = download(video_id)

    # 영상 분석 시각화
    video_point = gazeVisualization(video_id, video_csv, video_only, audio_only)
    print(video_point)
