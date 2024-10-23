from video_download import download
from video_detect import detect
from video_gaze_visualization import gazeVisualization
from video_score_cluster import score_cluster
import sys
import json

def main():

    print("영상 다운 시작")
    video_only, audio_only, video_filename = download(video_id)
    print(video_only, audio_only, video_filename)
    print("영상 다운 끝")

    print("영상 분할 시작")
    sceneTime = detect(video_id, video_only, video_filename)
    print("영상 분할 끝")

    print("영상 점수 및 클러스터 이미지 저장 시작")
    attention_score_list = score_cluster(video_id, video_csv, sceneTime)
    print("영상 점수 및 클러스터 이미지 저장 끝")
    
    print("영상 분석 시각화 시작")
    video_point = gazeVisualization(video_id, video_csv, video_only, audio_only, video_width, video_height)
    print("영상 분석 시각화 끝")


    print("최종적으로 반환할 값은 JSON 형식으로 반환")
    result = {
        "attention_score_list": attention_score_list,
        "video_point": video_point
    }

    # JSON 출력
    print(json.dumps(result))

if __name__ == "__main__":
    
    # UrEHWclh7Co 삼성카드
    # 0gkPFSvVvFw 전란
    # fRaIcUhaXXQ 핫초코
    # video_id = "0gkPFSvVvFw"
    # video_csv = "0gkPFSvVvFw_2024-10-12-18-56-44.csv"

    video_id = "0gkPFSvVvFw"
    video_csv = "0gkPFSvVvFw_2024-10-12-18-56-44.csv"
    video_width, video_height = 965, 543

    main()