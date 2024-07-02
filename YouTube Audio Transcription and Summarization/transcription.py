from pytube import YouTube
from pydub import AudioSegment
import os
import whisper
from transformers import pipeline

# Set the path to ffmpeg and ffprobe explicitly
ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe"
ffprobe_path = "C:/ffmpeg/bin/ffprobe.exe"

AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

def download_audio_youtube(url, output_path='audio.wav'):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename='audio.mp4')
        audio = AudioSegment.from_file('audio.mp4')
        audio.export(output_path, format='wav')
        os.remove('audio.mp4')
        return output_path
    except Exception as e:
        print(f"An error occurred during the download or conversion process: {e}")
        return None

def transcribe_audio(file_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        return result['text']
    except Exception as e:
        print(f"An error occurred during the transcription process: {e}")
        return None

def summarize_text(text):
    try:
        summarizer = pipeline("summarization")
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"An error occurred during the summarization process: {e}")
        return None

def save_to_file(filename, transcription, summary):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Transcription:\n")
            file.write(transcription + "\n\n")
            file.write("Summary:\n")
            file.write(summary + "\n")
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to file: {e}")

def main(youtube_url):
    audio_path = download_audio_youtube(youtube_url)
    if audio_path and os.path.exists(audio_path):
        transcription = transcribe_audio(audio_path)
        if transcription:
            summary = summarize_text(transcription)
            if summary:
                print("Transcription and Summary generated successfully.")
                save_to_file('transcription_summary.txt', transcription, summary)
                os.system('start transcription_summary.txt')  # For Windows
            
            else:
                print("Summarization failed.")
        else:
            print("Transcription failed.")
    else:
        print("Audio download failed.")

if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    main(youtube_url)
#https://youtu.be/N-kHHGAT2AE?si=Ex0CzR5Puijvc0OM