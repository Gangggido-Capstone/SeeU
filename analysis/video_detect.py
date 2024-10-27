from video_download import download

from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images
from concurrent.futures import ProcessPoolExecutor

import os
import cv2
import csv

def split_scene(video_path, start_time, end_time, output_dir, scene_number):
    output_file = os.path.join(output_dir, f'scene_{scene_number:03d}.mp4')
    command = f'ffmpeg -i "{video_path}" -ss {start_time} -to {end_time} -c copy "{output_file}" -y'
    os.system(command)

def split_video_parallel(video_path, scene_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # 병렬로 분할 작업 실행
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(split_scene, video_path, start.get_seconds(), end.get_seconds(), output_dir, i + 1)
            for i, (start, end) in enumerate(scene_list)
        ]
        # 모든 작업이 완료될 때까지 기다림
        for future in futures:
            future.result()

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_dir, 'README.md')):
        current_dir = os.path.abspath(os.path.join(current_dir, '..'))
    return current_dir

def detect(video_id, video_only):
    try:
        # 루트 경로 가져오기
        root_path = get_root_path()

        # split_video 디렉토리 경로 설정
        split_video_directory = os.path.join(root_path, "Data", "video", video_id, "split_video")
        sceneTime = []

        if not os.path.exists(split_video_directory):
            # 영상 불러오기
            video = open_video(video_only)

            # 초당 프레임 수
            fps = cv2.VideoCapture(video_only).get(cv2.CAP_PROP_FPS)  
            # 디텍터 생성, 임계값 27, 장면 당 최소 프레임 수, 분할 영상 최소 5초
            content_detector = ContentDetector(threshold=27, min_scene_len = fps * 5)

            # Scene Manager 생성
            scene_manager = SceneManager()
            scene_manager.add_detector(content_detector)

            # detect 수행 (영상의 처음부터 끝까지 detect) =============================================
            scene_manager.detect_scenes(video, show_progress=True)

            # `get_scene_list` 리스트의 시작과 끝 timecode pairs 을 리턴
            scene_list = scene_manager.get_scene_list()
            print(scene_list)
            
            scene_times_csv = os.path.join(root_path, "Data", "video", video_id, "split_video", "scene_times.csv")
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
            split_video_parallel(video_only, scene_list, split_video_directory)

            # 썸네일 만들기 (jpg 파일로 저장)
            save_images(
                scene_list, # 장면 리스트 [(시작, 끝)]
                video, # 영상
                num_images=1, # 각 장면 당 이미지 개수
                image_name_template=f'{video_id}_$SCENE_NUMBER', # 결과 이미지 파일 이름
                output_dir=os.path.join(root_path, "Data", "video", video_id, "thumbnails") # 결과 디렉토리 이름
            )

            print(f"{video_id} Video segmentation completed")
            
        else:
            print(f"{video_id} split video already exists. Skip download.")

            scene_times_csv = os.path.join(root_path, "Data", "video", video_id, "split_video", "scene_times.csv")

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

    # UrEHWclh7Co 삼성카드
    # 0gkPFSvVvFw 전란
    # fRaIcUhaXXQ 핫초코
    video_id = "jWQx2f-CErU"
    
    # 영상 다운
    video_only = download(video_id)

    # 영상 분할
    sceneTime = detect(video_id, video_only)
