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

    video_only = os.path.join(video_dir, "video.mp4")
    audio_only = os.path.join(video_dir, "audio.m4a")
    video_filename = os.path.join(video_dir, f"{video_id}.mp4")


    # 파일이 이미 존재하는지 확인
    if not os.path.exists(video_filename):
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

        try:
            # ffmpeg를 사용해 비디오와 오디오 병합
            ffmpeg_path = "C:/ffmpeg/bin/ffmpeg"
            merge_command = [
                ffmpeg_path,
                '-i', video_only,  # 좌표가 그려진 비디오 파일
                '-i', audio_only,  # 입력 오디오 파일
                '-c:v', 'copy',  # 비디오를 재인코딩하지 않고 복사
                '-c:a', 'aac',  # 오디오를 AAC 형식으로 변환
                '-b:a', '192k',  # 오디오 비트레이트 설정
                '-r', '24',  # 비디오 프레임 속도 설정
                '-preset', 'ultrafast',  # 초고속 인코딩 옵션
                '-threads', '4',  # CPU 스레드 개수 지정
                '-vsync', 'cfr',  # 고정 프레임 속도 동기화
                '-map', '0:v:0',  # 비디오 스트림을 첫 번째 입력에서 가져오기
                '-map', '1:a:0',  # 오디오 스트림을 두 번째 입력에서 가져오기
                '-shortest',  # 가장 짧은 스트림 기준으로 맞추기
                video_filename  # 최종 출력 파일 경로
            ]

            print("subprocess run")
            # ffmpeg 명령어 실행 (비동기)
            ffmpeg_process = subprocess.Popen(merge_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = ffmpeg_process.communicate(timeout=400)
            print("subprocess end")

            if ffmpeg_process.returncode != 0:
                print(f"FFmpeg error: {stderr}")
            else:
                print(f"FFmpeg success: {stdout}")
                print(f"download: {video_filename}")

        except subprocess.TimeoutExpired:
            ffmpeg_process.kill()  # 타임아웃이 발생하면 프로세스 강제 종료
            print("FFmpeg Time Out")
            
        finally:
            ffmpeg_process.kill()

    else:
        print(f"{video_filename} The file already exists.")

    return video_only, audio_only, video_filename
    


if __name__ == "__main__":
  
    # video_id, video_csv는 스프링에서 넘겨야 함
    # UrEHWclh7Co 삼성카드
    # 0gkPFSvVvFw 전란
    # fRaIcUhaXXQ 핫초코
    # video_id = "0gkPFSvVvFw"
    # video_csv = "0gkPFSvVvFw_2024-10-12-18-56-44.csv"
    video_id = "fRaIcUhaXXQ"
    
    video_only, audio_only, video_filename = download(video_id)

    