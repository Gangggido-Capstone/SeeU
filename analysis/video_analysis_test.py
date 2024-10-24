from video_download import download
from video_detect import detect
from video_gaze_visualization import gazeVisualization
from video_score_cluster import score_cluster
import json

def main():
    print("download start=====================================")
    video_only, audio_only, video_filename = download(video_id)
    print("download end=======================================")

    print("detect start=======================================")
    sceneTime = detect(video_id, video_only, video_filename)
    print("detect end=========================================")

    print("score_cluster start================================")
    attention_score_list = score_cluster(video_id, video_csv, sceneTime)
    print("score_cluster end==================================")
    
    print("gazeVisualization start============================")
    video_point = gazeVisualization(video_id, video_csv, video_only, audio_only, video_width, video_height)
    print("gazeVisualization end==============================")

    result = {
        "attention_score_list": attention_score_list,
        "video_point": video_point
    }
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