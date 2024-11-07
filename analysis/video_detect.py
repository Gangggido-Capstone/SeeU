from video_download import download

from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images
import os
import cv2
import csv

def split_scene(video_path, start_time, end_time, output_dir, scene_number):
    output_file = os.path.join(output_dir, f'scene_{scene_number:03d}.mp4')
    command = f'ffmpeg -i "{video_path}" -ss {start_time} -to {end_time} -c copy "{output_file}" -y'
    os.system(command)

def split_video(video_path, scene_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)
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
        root_path = get_root_path()

        # split_video 디렉토리 경로 설정
        split_video_directory = os.path.join(root_path, "data", "video", video_id, "split_video")
        sceneTime = []

        if not os.path.exists(split_video_directory):
            video = open_video(video_only)
            fps = cv2.VideoCapture(video_only).get(cv2.CAP_PROP_FPS)  
            content_detector = ContentDetector(threshold=25, min_scene_len = fps * 4) # 디텍터 생성, 임계값 25, 장면 당 최소 프레임 수, 분할 영상 최소 4초

            scene_manager = SceneManager()
            scene_manager.add_detector(content_detector)
            scene_manager.detect_scenes(video, show_progress=True)

            scene_list = scene_manager.get_scene_list()
            print(scene_list)
            
            scene_times_csv = os.path.join(root_path, "data", "video", video_id, "split_video", "scene_times.csv")
            os.makedirs(os.path.dirname(scene_times_csv), exist_ok=True)
            with open(scene_times_csv, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Start", "End"])

                for scene in scene_list:
                    start, end = scene
                    if start.get_seconds() == 0:
                        start_time = round(start.get_seconds(), 4)
                    else:
                        start_time = round(start.get_seconds(), 4) - 0.3

                    end_time = round(end.get_seconds(), 4)

                    writer.writerow([start_time, end_time])
                    sceneTime.append((start_time, end_time))

                if not sceneTime:
                    video_capture = cv2.VideoCapture(video_only)
                    total_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
                    fps = video_capture.get(cv2.CAP_PROP_FPS)
                    
                    # 영상의 총 길이를 초 단위로 계산
                    total_duration = total_frames / fps
                    
                    # 시작 시간 0, 끝 시간은 영상의 총 길이
                    start_time = 0.0
                    end_time = round(total_duration, 4)  # 소수점 이하 4자리까지 반올림

                    writer.writerow([start_time, end_time])
                    sceneTime.append((start_time, end_time))
                    
                    video_capture.release()

            print("Split time from CSV file:", sceneTime)

            # 영상 자르기
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

if __name__ == "__main__":
    video_id = ""
    
    # 영상 다운
    video_only = download(video_id)

    # 영상 분할
    sceneTime = detect(video_id, video_only)
