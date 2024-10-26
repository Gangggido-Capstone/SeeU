import os
import yt_dlp
import subprocess

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_dir, 'README.md')):
        current_dir = os.path.abspath(os.path.join(current_dir, '..'))
    return current_dir

def download(video_id):
    root_path = get_root_path()
    video_url = f"https://youtu.be/{video_id}"

    video_dir = os.path.join(root_path, "Data", "video", video_id)

    audio_only = os.path.join(video_dir, "audio.m4a")
    video_only = os.path.join(video_dir, f"{video_id}.mp4")

    if not os.path.exists(video_only):
        os.makedirs(os.path.join(root_path, "Data", "video", video_id), exist_ok=True)

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

    else:
        print(f"{video_only} The file already exists.")

    return video_only, audio_only
    

if __name__ == "__main__":
  
    # video_id, video_csv는 스프링에서 넘겨야 함
    # UrEHWclh7Co 삼성카드
    # 0gkPFSvVvFw 전란
    # fRaIcUhaXXQ 핫초코
    # video_id = "0gkPFSvVvFw"
    # video_csv = "0gkPFSvVvFw_2024-10-12-18-56-44.csv"
    video_id = "fRaIcUhaXXQ"
    
    video_only, audio_only = download(video_id)

    