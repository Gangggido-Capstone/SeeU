from video_download import download
from video_detect import detect
from sklearn.cluster import DBSCAN
import pandas as pd
import os

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_dir, 'README.md')):
        current_dir = os.path.abspath(os.path.join(current_dir, '..'))
    return current_dir

def score_cluster(video_id, video_csv, sceneTime):
    root_path = get_root_path()

    # CSV 파일 불러오기
    csv_path = os.path.join(root_path, "Data", "GazeData")
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

        # dbscan = DBSCAN(eps=30 , min_samples=5)
        dbscan = DBSCAN(eps=27, min_samples=5)
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

        # 클러스터 점수 * 0.7 + Attention 비율 점수 * 0.2
        res = round(((focus_score1 * 0.8) + (focus_score2 * 0.2)) * 100, 2)
        final_score.append(res)

        # print("start: " + str(start) + ", " + "end: " + str(end))
        print(f"({index}) Time: {start:.2f} ~ {end:.2f}, Attention Score: {res}")

    # 리스트에 저장해 반환
    atention_score_list = []
    # split_video 디렉토리 경로 설정
    split_video_directory = os.path.join(root_path, "Data", "video", video_id, "split_video")
    thumbnails_dir = os.path.join(root_path, "Data", "video", video_id, "thumbnails")
    # final_score를 기준으로 내림차순 정렬
    sorted_data = sorted(enumerate(zip(sceneTime, final_score)), key=lambda x: x[1][1], reverse=True)
    for i, (_, score) in sorted_data:
        if score == 0:
            continue
        atention_score_list.append((f"{split_video_directory}\\{video_id}-Scene-{i+1:03}.mp4", f"{thumbnails_dir}\\{video_id}_{i+1:03}.jpg", score))

    return atention_score_list


if __name__ == "__main__":
    # UrEHWclh7Co 삼성카드
    # 0gkPFSvVvFw 전란
    # fRaIcUhaXXQ 핫초코

    # video_id = "fRaIcUhaXXQ"
    # video_csv = "fRaIcUhaXXQ_2024-10-20-16-50-56.csv"
    video_id = "iiIcTPoIoZk"
    video_csv = "iiIcTPoIoZk_2024-10-26-16-44-40.csv"

    # 영상 다운
    video_only = download(video_id)

    # 영상 분할
    sceneTime = detect(video_id, video_only)

    # 영상 점수 및 클러스터 이미지 저장
    atention_score_list = score_cluster(video_id, video_csv, sceneTime)
    for a in atention_score_list:
        print(a)