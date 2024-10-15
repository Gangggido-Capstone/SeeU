import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import pandas as pd

# CSV 파일 경로
csv_path = "Data\\GazeData\\0gkPFSvVvFw_2024-10-12-18-56-44.csv"
dt = "2024-10-12-18-56-44"

# CSV 파일 불러오기
data = pd.read_csv(csv_path)

# 0 ~ 67초 사이(영상1)의 데이터만 선택
filtered_data = data[(data['Time'] >= 0) & (data['Time'] <= 67)]

# 유효한 X, Y 값이 있는 행만 선택
valid_data = filtered_data.dropna(subset=['X', 'Y'])

# X, Y 값을 정수로 변환
x_values = valid_data['X'].astype(int).tolist()
y_values = valid_data['Y'].astype(int).tolist()

# DBSCAN 알고리즘 적용
gaze_data = list(zip(x_values, y_values))
dbscan = DBSCAN(eps=30 , min_samples=5)
labels = dbscan.fit_predict(gaze_data)

# 클러스터 개수 출력
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(f"Number of clusters found: {n_clusters}")

# 최대(가장 많은 시선이 포함된) 클러스터의 정보
max_n = 0 # 클러스터에 속하는 시선의 수
xx = 0    # 클러스터 바운딩박스의 x좌표
yy = 0    # 클러스터 바운딩박스의 y좌표
ww = 0    # 클러스터 바운딩박스의 너비
hh = 0    # 클러스터 바운딩박스의 높이

# 라벨 집합
unique_labels = set(labels)

# 최대 클러스터 구하기
for label in unique_labels:
    # 클러스터에 속하지 않는 포인트
    if label == -1:
        continue

    cluster_points = []

    # label번 클러스터에 속한 점만 필터링
    for i in range(200):
      if labels[i] == label:
        cluster_points.append(gaze_data[i])

    # 최대 클러스터 정보 업데이트
    n = len(cluster_points)
    if n > max_n:
      max_n = n

      # 바운딩 박스 계산
      xs = [point[0] for point in cluster_points]
      ys = [point[1] for point in cluster_points]
      xx = np.min(xs)
      yy = np.min(ys)
      ww = np.max(xs) - xx
      hh = np.max(ys) - yy

print(xx, yy, ww, hh)

fig, ax = plt.subplots()

# 최대 클러스터의 바운딩박스 그리기
rect = patches.Rectangle((xx, yy), ww, hh, linewidth=0.1, edgecolor='black', facecolor='none')
ax.add_patch(rect)

# gaze_data를 Numpy 배열로 변환
gaze_data = np.array(gaze_data)

# 시선 포인트들 그리기
ax.scatter(gaze_data[:, 0], gaze_data[:, 1], c=labels, cmap='rainbow')
plt.show()

















# # 그래프 설정
# fig, ax = plt.subplots(figsize=(8, 6))

# # 사각형 그리기
# w, h = 965, 543
# rect = patches.Rectangle((0, 0), w, h, linewidth=0.1, edgecolor='black', facecolor='none')
# ax.add_patch(rect)

# # 시선점들 그리기
# sc = ax.scatter(x_values, y_values, c=labels, cmap='rainbow', s=10)
# plt.colorbar(sc, ax=ax, label='Cluster Label')
# plt.title('DBSCAN Clustering of Gaze Data (0-67s)')
# plt.xlabel('X Coordinate')
# plt.ylabel('Y Coordinate')

# # 그래프 보여주기
# plt.show()

# import numpy as np
# from sklearn.cluster import DBSCAN
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import cv2

# # 총 200개의 좌표 생성
# number_of_points = [20, 10, 20, 10, 100, 40]
# x_ranges = [(0.3, 0.7), (0.4, 0.5), (0.2, 0.5), (0.9, 1.0), (0.7, 0.8), (0.2, 0.3)]
# y_ranges = [(0.3, 0.9), (0.2, 0.5), (0.2, 0.6), (0.1, 0.2), (0.2, 0.7), (0.1, 0.3)]
# points = []

# for i in range(6):
#   for j in range(number_of_points[i]):
#     x = np.random.uniform(low=x_ranges[i][0], high=x_ranges[i][1])
#     y = np.random.uniform(low=y_ranges[i][0], high=y_ranges[i][1])
#     points.append((x, y))

# # 노이즈 추가
# noise = np.random.uniform(low=0.0, high=0.15, size=(200, 2))

# # 시선 더미 데이터
# gaze_data = points + noise
# print(gaze_data)


# # DBSCAN 알고리즘 사용하여 시선데이터 클러스터링
# dbscan = DBSCAN(eps=0.1, min_samples=20)
# labels = dbscan.fit_predict(gaze_data)

# # 클러스터 개수 출력
# n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
# print(f"Number of clusters found: {n_clusters}")

