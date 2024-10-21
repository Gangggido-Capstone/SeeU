import sys
from video_download import download
from video_detect import detect
from video_gaze_visualization import gazeVisualization
from video_score_cluster import score_cluster


# video_id, video_csv는 스프링에서 넘겨야 함 ============
# UrEHWclh7Co 삼성카드
# 0gkPFSvVvFw 전란
# fRaIcUhaXXQ 핫초코

video_id = "0gkPFSvVvFw"
video_csv = "0gkPFSvVvFw_2024-10-12-18-56-44.csv"

# =====================================================


#if len(sys.argv) != 3:
#    print("전달된 인수 초과")
#    sys.exit(1)

#video_id = sys.argv[1]  # 첫 번째 인자는 video_id
#video_csv = sys.argv[2]  # 두 번째 인자는 video_csv


# 영상 다운
video_only, audio_only, video_filename = download(video_id)

# 영상 분할
sceneTime = detect(video_id, video_only, video_filename)

# 영상 점수 및 클러스터 이미지 저장
atention_score_list = score_cluster(video_id, video_csv, sceneTime)

# 영상 분석 시각화
video_point = gazeVisualization(video_id, video_csv, video_only, audio_only)
print(video_point)


# 아래 값 스프링에 전달해야 함 ================
for atention_score in atention_score_list:
    print(atention_score)
print(video_point)