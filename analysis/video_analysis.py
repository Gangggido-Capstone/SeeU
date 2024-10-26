from video_download import download
from video_detect import detect
from video_gaze_visualization import gazeVisualization
from video_score_cluster import score_cluster
import sys
import json
import time

def main():
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

    print("================================= download start =================================")
    video_only, audio_only = download(video_id)
    download_end = time.time()
    print(f"download end: {download_end - start:.5f} sec")

    print("================================== detect start ==================================")
    sceneTime = detect(video_id, video_only)
    detect_end = time.time()
    print(f"detect end: {detect_end - start:.5f} sec")

    print("============================== score cluster start ==============================")
    attention_score_list = score_cluster(video_id, video_csv, sceneTime)
    cluster_end = time.time()
    print(f"score cluster end: {cluster_end - start:.5f} sec")

    print("================================== point start ==================================")
    video_point = gazeVisualization(video_id, video_csv, video_only, audio_only, video_width, video_height)
    point_end = time.time()
    print(f"point end: {point_end - start:.5f} sec")

    # JSON
    result = {
        "attention_score_list": attention_score_list,
        "video_point": video_point
    }
    print(json.dumps(result))

    end = time.time()
    print(f"python script end: {end - start:.5f} sec")

if __name__ == "__main__":
    main()