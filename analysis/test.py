import sys
import json
import time
import os
import yt_dlp
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images

import os
import cv2
import csv

from sklearn.cluster import DBSCAN
import pandas as pd
import os


print(f"python script start")
start = time.time()

if len(sys.argv) < 5:
    print("Warning: Missing required arguments.")
    print("video_width, video_height = 965, 543")
    video_width, video_height = 965, 543
else:
    video_width, video_height = int(float(sys.argv[3])), int(float(sys.argv[4]))

video_id, video_csv = sys.argv[1], sys.argv[2]

print("video_id: " + str(video_id))
print("video_csv: " + str(video_csv))
print("video_width: " + str(video_width))
print("video_height: " + str(video_height))

print("video_id, video_csv, video_width, video_height = " + str(video_id) + str(video_csv) + str(video_width) + str(video_height) )

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    root_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(root_dir, 'README.md')):
        root_dir = os.path.abspath(os.path.join(root_dir, '..'))
    current_dir = os.path.join(root_dir, "frontend", "public")
    return current_dir

def download(video_id):
    root_path = get_root_path()
    video_url = f"https://youtu.be/{video_id}"

    video_dir = os.path.join(root_path, "data", "video", video_id)
    video_only = os.path.join(video_dir, f"{video_id}.mp4")

    if not os.path.exists(video_only):
        os.makedirs(os.path.join(root_path, "data", "video", video_id), exist_ok=True)

        # yt-dlp 옵션 설정: 비디오만 다운로드
        ydl_opts_video = {
            'format': 'bestvideo',
            'outtmpl': video_only,
            'quiet': True
        }

        # 비디오 다운로드
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([video_url])

    else:
        print(f"{video_only} The file already exists.")

    return video_only

print("================================= download start =================================")
video_only = download(video_id)
download_end = time.time()
print(f"================ download end: {download_end - start:.5f} sec ================")

def split_scene(video_path, start_time, end_time, output_dir, scene_number):
    output_file = os.path.join(output_dir, f'scene_{scene_number:03d}.mp4')
    command = f'ffmpeg -i "{video_path}" -ss {start_time} -to {end_time} -c copy "{output_file}" -y'
    os.system(command)

def split_video(video_path, scene_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 분할 작업을 순차적으로 실행
    for i, (start, end) in enumerate(scene_list):
        split_scene(video_path, start, end, output_dir, i + 1)

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    root_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(root_dir, 'README.md')):
        root_dir = os.path.abspath(os.path.join(root_dir, '..'))
    current_dir = os.path.join(root_dir, "frontend", "public")
    return current_dir

def detect(video_id, video_only):
    try:
        # 루트 경로 가져오기
        root_path = get_root_path()

        # split_video 디렉토리 경로 설정
        split_video_directory = os.path.join(root_path, "data", "video", video_id, "split_video")
        sceneTime = []

        if not os.path.exists(split_video_directory):
            # 영상 불러오기
            video = open_video(video_only)

            # 초당 프레임 수
            fps = cv2.VideoCapture(video_only).get(cv2.CAP_PROP_FPS)  
            # 디텍터 생성, 임계값 25, 장면 당 최소 프레임 수, 분할 영상 최소 4초
            content_detector = ContentDetector(threshold=25, min_scene_len = fps * 4)

            # Scene Manager 생성
            scene_manager = SceneManager()
            scene_manager.add_detector(content_detector)

            # detect 수행 (영상의 처음부터 끝까지 detect) =============================================
            scene_manager.detect_scenes(video, show_progress=True)

            # `get_scene_list` 리스트의 시작과 끝 timecode pairs 을 리턴
            scene_list = scene_manager.get_scene_list()
            print(scene_list)
            
            scene_times_csv = os.path.join(root_path, "data", "video", video_id, "split_video", "scene_times.csv")
            os.makedirs(os.path.dirname(scene_times_csv), exist_ok=True)
            with open(scene_times_csv, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Start", "End"])  # CSV 헤더

                for scene in scene_list:
                    start, end = scene
                    # 시작 시간과 끝 시간을 초 단위로 반올림하여 저장
                    if start.get_seconds() == 0:
                        start_time = round(start.get_seconds(), 4)
                    else:
                        start_time = round(start.get_seconds(), 4) - 0.3

                    end_time = round(end.get_seconds(), 4)

                    writer.writerow([start_time, end_time])
                    sceneTime.append((start_time, end_time))

                if not sceneTime:
                    # 영상의 길이를 가져오기 위해 VideoCapture 사용
                    video_capture = cv2.VideoCapture(video_only)
                    total_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)  # 총 프레임 수 가져오기
                    fps = video_capture.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수 가져오기
                    
                    # 영상의 총 길이를 초 단위로 계산
                    total_duration = total_frames / fps
                    
                    # 시작 시간 0, 끝 시간은 영상의 총 길이
                    start_time = 0.0
                    end_time = round(total_duration, 4)  # 소수점 이하 4자리까지 반올림

                    writer.writerow([start_time, end_time])  # CSV 파일에 시작 시간과 끝 시간 저장
                    sceneTime.append((start_time, end_time))  # sceneTime 리스트에 시작 시간과 끝 시간 추가
                    
                    video_capture.release()  # VideoCapture 객체 해제

            print("Split time from CSV file:", sceneTime)

            # # 영상 자르기 (파일로 저장)
            # split_video_ffmpeg(video_only, scene_list, output_dir=split_video_directory,show_progress=True)

            # 영상 자르기 (병렬 처리 사용)
            split_video(video_only, scene_list, split_video_directory)

            # 썸네일 만들기 (jpg 파일로 저장)
            save_images(
                scene_list, # 장면 리스트 [(시작, 끝)]
                video, # 영상
                num_images=1, # 각 장면 당 이미지 개수
                image_name_template=f'{video_id}_$SCENE_NUMBER', # 결과 이미지 파일 이름
                output_dir=os.path.join(root_path, "data", "video", video_id, "thumbnails") # 결과 디렉토리 이름
            )

            print(f"{video_id} Video segmentation completed")
            
        else:
            print(f"{video_id} split video already exists. Skip download.")

            scene_times_csv = os.path.join(root_path, "data", "video", video_id, "split_video", "scene_times.csv")

            if os.path.exists(scene_times_csv):
                # CSV 파일에서 분할된 시간 불러오기
                with open(scene_times_csv, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader)  # 헤더 건너뛰기
                    
                    for row in reader:
                        start_time = float(row[0])
                        end_time = float(row[1])
                        sceneTime.append((start_time, end_time))

                print("Split time from CSV file:", sceneTime)

            else:
                print(f"scene_times.csv of {video_id} does not exist")
        
        return sceneTime
    except Exception as e:
        print(f"Error in Detect function: {str(e)}")
        raise e
    

print("================================== detect start ==================================")
sceneTime = detect(video_id, video_only)
detect_end = time.time()
print(f"================ detect end: {detect_end - start:.5f} sec ================")

def score_cluster(video_id, video_csv, sceneTime):
    root_path = get_root_path()

    # CSV 파일 불러오기
    csv_path = os.path.join(root_path, "data", "GazeData")
    gaze_csv = pd.read_csv(os.path.join(csv_path, video_csv))
    
    final_score = []

    # 분할 영상 별 집중도 점수 및 클러스터 시각화 이미지 저장
    for index, scene in enumerate(sceneTime):
        start, end = scene
        filtered_data = gaze_csv[(gaze_csv['Time'] >= start) & (gaze_csv['Time'] <= end)]
        valid_data = filtered_data.dropna(subset=['X', 'Y'])

        x_values = valid_data['X'].astype(int).tolist()
        y_values = valid_data['Y'].astype(int).tolist()

        # DBSCAN 알고리즘 적용
        gaze_data = list(zip(x_values, y_values))

        if len(gaze_data) == 0:
            print(f"Scene {index+1}: No valid gaze data available.")
            final_score.append(0)
            continue  # 다음 씬으로 넘어감

        # dbscan = DBSCAN(eps=30 , min_samples=6)
        dbscan = DBSCAN(eps=27, min_samples=6)
        labels = dbscan.fit_predict(gaze_data)

        # DBSCAN 클러스터 점수
        # labels 배열에서 -1 값은 클러스터에 속하지 않는 노이즈(즉, 집중되지 않은 점)를 의미
        # labels != -1 조건을 만족하는 점들은 클러스터에 속하는 점
        num_focus_points = sum(labels != -1)
        focus_score1 = num_focus_points / len(labels)

        # Attention 값(0) 비율 점수
        attention_values = valid_data['Attention'].astype(int).tolist() 
        zero_data = attention_values.count(0)
        focus_score2 = zero_data / len(attention_values)

        # 클러스터 점수 * 0.7 + Attention 비율 점수 * 0.3
        res = round(((focus_score1 * 0.7) + (focus_score2 * 0.3)) * 100, 2)
        final_score.append(res)

        # print("start: " + str(start) + ", " + "end: " + str(end))
        print(f"({index + 1}) Time: {start:.2f} ~ {end:.2f}, Attention Score: {res}")

    # 리스트에 저장해 반환
    atention_score_list = []
    # split_video 디렉토리 경로 설정
    split_video_directory = os.path.join(video_id, "split_video")
    thumbnails_dir = os.path.join(video_id, "thumbnails")
    # final_score를 기준으로 내림차순 정렬
    sorted_data = sorted(enumerate(zip(sceneTime, final_score)), key=lambda x: x[1][1], reverse=True)
    for i, (_, score) in sorted_data:
        if len(sorted_data) == 1:
            atention_score_list.append((f"{video_id}\\{video_id}.mp4", "null", score))
        else:
            atention_score_list.append((f"{split_video_directory}\\scene_{i+1:03}.mp4", f"{thumbnails_dir}\\{video_id}_{i+1:03}.jpg", score))

    return atention_score_list

print("============================== score cluster start ==============================")
attention_score_list = score_cluster(video_id, video_csv, sceneTime)
cluster_end = time.time()
print(f"================ score cluster end: {cluster_end - start:.5f} sec ================")

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


print("================================== point start ==================================")
video_point = gazeVisualization(video_id, video_csv, video_only, video_width, video_height)

point_end = time.time()
print(f"================ point end: {point_end - start:.5f} sec ==================")

result = {
    "attention_score_list": attention_score_list,
    "video_point": video_point
}

print(json.dumps(result))

    
end = time.time()
print(f"python script end: {end - start:.5f} sec")
