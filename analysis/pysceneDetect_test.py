from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images
from scenedetect.video_splitter import split_video_ffmpeg
from video_download import download
import os
import cv2
# "HdOhm3v4Sg8"
# 0gkPFSvVvFw 전란
video_id = "0gkPFSvVvFw"

# 유튜브 영상 다운로드
video_only, audio_only, video_filename = download(video_id)

# 파일이 이미 존재하는지 확인
split_video_directory = f"analysis/video/{video_id}/split_video"

if not os.path.exists(split_video_directory):
    # 영상 불러오기
    video = open_video(video_filename)

    # 초당 프레임 수
    fps = cv2.VideoCapture(video_only).get(cv2.CAP_PROP_FPS)  
    f = fps * 8 # 장면 당 최소 프레임 수
    # 디텍터 생성, 임계값 35, 장면 당 최소 프레임 수 
    content_detector = ContentDetector(threshold=35, min_scene_len=f)

    # Scene Manager 생성
    scene_manager = SceneManager()
    scene_manager.add_detector(content_detector)

    # detect 수행 (영상의 처음부터 끝까지 detect)
    scene_manager.detect_scenes(video, show_progress=True)

    # `get_scene_list` 리스트의 시작과 끝 timecode pairs 을 리턴
    scene_list = scene_manager.get_scene_list()
    print(scene_list)
    #장면 시작하는 시간을 저장하는 리스트
    sceneTime = [] 

    # 장면 분할 결과 출력
    for scene in scene_list:
        start, end = scene
        if start.get_seconds()== 0:
            sceneTime.append(round(start.get_seconds(), 4))
        else:
            sceneTime.append(round(start.get_seconds(), 4) - 0.3)

        print(start, "~", end)   
    print()    
    #이 값은 몽고디비에 같이 저장 할 수 있도록 해야 함
    print(sceneTime)

    # 영상 자르기 (파일로 저장)
    split_video_ffmpeg(video_filename, scene_list, output_dir=split_video_directory,show_progress=True)

    # 썸네일 만들기 (jpg 파일로 저장)
    save_images(
        scene_list, # 장면 리스트 [(시작, 끝)]
        video, # 영상
        num_images=1, # 각 장면 당 이미지 개수
        image_name_template=f'{video_id}_$SCENE_NUMBER', # 결과 이미지 파일 이름
        output_dir=f'analysis/video/{video_id}/thumbnails') # 결과 디렉토리 이름

    print(f"{video_id} 영상 분할 완료")
else:
    print(f"{video_id} split_video가 이미 존재합니다. 다운로드를 건너뜁니다.")