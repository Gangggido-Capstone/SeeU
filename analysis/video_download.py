import os
import yt_dlp
import subprocess
import pandas as pd
from datetime import datetime

# CSV 파일 경로
csv_file = "Data\\GazeData\\RoER-ab1QYw_2024-10-08-22-02-29.csv"

# CSV 데이터 로드
df = pd.read_csv(csv_file)

# 1. 유튜브 영상 다운로드
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
video_id = "RoER-ab1QYw"
video_url = f"https://youtu.be/{video_id}"  # 유튜브 영상 URL
video_filename = f"analysis/input_video/{video_id}_{timestamp}.mp4"  # 최종 저장할 비디오 파일 경로
video_only = f"analysis/input_video/video_only_{timestamp}.mp4"  # 비디오 파일 경로
audio_only = f"analysis/input_video/audio_only_{timestamp}.m4a"  # 오디오 파일 경로

# yt-dlp 옵션 설정: 비디오와 오디오를 별도로 다운로드
ydl_opts_video = {
    'format': 'bestvideo',
    'outtmpl': video_only,
}

ydl_opts_audio = {
    'format': 'bestaudio',
    'outtmpl': audio_only,
}

# 비디오 다운로드
with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
    ydl.download([video_url])

# 오디오 다운로드
with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
    ydl.download([video_url])

# ffmpeg를 사용해 비디오와 오디오 병합
merge_command = [
    'ffmpeg',
    '-i', video_only,  # 좌표가 그려진 비디오 파일
    '-i', audio_only,         # 입력 오디오 파일
    '-c:v', 'libx264',        # 비디오를 H.264로 재인코딩
    '-preset', 'fast',        # 빠른 인코딩 옵션
    '-c:a', 'aac',            # 오디오를 AAC 형식으로 변환
    '-b:a', '192k',           # 오디오 비트레이트 설정
    '-r', '30',               # 비디오 프레임 속도 강제 설정 (30fps, 고정 프레임 속도)
    '-vsync', 'cfr',          # 고정 프레임 속도 동기화
    '-map', '0:v:0',          # 비디오 스트림을 첫 번째 입력에서 가져오기
    '-map', '1:a:0',          # 오디오 스트림을 두 번째 입력에서 가져오기
    '-shortest',              # 가장 짧은 스트림 기준으로 맞추기
    video_filename            # 최종 출력 파일 경로
]

# 병합 명령어 실행
subprocess.run(merge_command)

# 병합 완료 후 비디오 및 오디오 파일 삭제
if os.path.exists(video_only):
    os.remove(video_only)
    print(f"{video_only} 파일이 삭제되었습니다.")

if os.path.exists(audio_only):
    os.remove(audio_only)
    print(f"{audio_only} 파일이 삭제되었습니다.")

print("좌표가 그려진 비디오와 오디오 병합 완료 및 파일 삭제")
