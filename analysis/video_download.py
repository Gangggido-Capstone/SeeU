import os
import yt_dlp

def get_root_path():
    # 현재 디렉토리에서 README.md 파일이 존재하는 경로를 루트로 설정
    root_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(root_dir, 'README.md')):
        root_dir = os.path.abspath(os.path.join(root_dir, '..'))
    current_dir = os.path.join(root_dir, "frontend", "public")
    return current_dir

def download(video_id):
    root_path = get_root_path()
    video_url = f"https://youtu.be/{video_id}"

    video_dir = os.path.join(root_path, "data", "video", video_id)
    video_only = os.path.join(video_dir, f"{video_id}.mp4")

    if not os.path.exists(video_only):
        os.makedirs(os.path.join(root_path, "data", "video", video_id), exist_ok=True)

        # yt-dlp 옵션 설정: 비디오만 다운로드
        ydl_opts_video = {
            'format': 'bestvideo',
            'outtmpl': video_only,
            'quiet': True,
        }

        # 비디오 다운로드
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([video_url])

    else:
        print(f"{video_only} The file already exists.")

    return video_only

    
if __name__ == "__main__":
    video_id = ""

    video_only = download(video_id)
