from video_download import download
from video_detect import detect
from video_gaze_visualization import gazeVisualization
from video_score_cluster import score_cluster
import sys
import json

def main():
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

    # 영상 다운
    video_only, audio_only, video_filename = download(video_id)
    print(video_only, audio_only, video_filename)
    # 영상 분할
    sceneTime = detect(video_id, video_only, video_filename)

    # 영상 점수 및 클러스터 이미지 저장
    attention_score_list = score_cluster(video_id, video_csv, sceneTime)

    # 영상 분석 시각화
    video_point = gazeVisualization(video_id, video_csv, video_only, audio_only, video_width, video_height)
    
    # 최종적으로 반환할 값은 JSON 형식으로 반환
    result = {
        "attention_score_list": attention_score_list,
        "video_point": video_point
    }
    
    # JSON 출력
    print(json.dumps(result))

if __name__ == "__main__":
    main()