import pretty_midi
import librosa
import numpy as np
import soundfile as sf
from fastapi import FastAPI
from fastapi.responses import FileResponse
from moviepy.editor import *

app = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "World"}


@app.get("/api/generate")
def main():
    # melody
    new_beat = pretty_midi.PrettyMIDI('.\\sample_data\\melody\\output.mid')  # 1
    standard = new_beat.instruments[0].notes[0].pitch
    # meme audio
    y, sr = librosa.load(".\\sample_data\\meme\\raw\\cat.wav")
    block_length = len(y) / sr
    print(block_length)
    # meme video
    clip = VideoFileClip(".\\sample_data\\meme\\raw\\cat_block.mp4")
    clip_duration = clip.duration
    # output
    n_audio = y
    final_clip = change_video(clip, clip_duration, len(n_audio) / sr)

    for instrument in new_beat.instruments:  # 2
        for note in instrument.notes:  # 3
            if note.pitch > 65:
                changed = change_audio(y, block_length, sr, standard - note.pitch, note.duration)
                n_audio = np.concatenate((n_audio, changed), axis=0)
                new_clip = change_video(clip, clip_duration, note.duration)
                final_clip = concatenate_videoclips([final_clip, new_clip])

    sf.write('.\\sample_data\\meme\\edited\\bgm.wav', n_audio, sr)
    background_music = AudioFileClip(".\\sample_data\\meme\\edited/bgm.wav")
    final_clip = final_clip.set_audio(background_music)
    final_clip.write_videofile(".\\sample_data\\output\\output.mp4", threads=32)
    return FileResponse(".\\sample_data\\output\\output.mp4")


def change_audio(y, block_length, sr, n_step, duration):
    y_pitch = librosa.effects.pitch_shift(y, sr, n_steps=n_step)
    y_slow = librosa.effects.time_stretch(y_pitch, block_length / duration)
    return y_slow


def change_video(clip, clip_duration, duration):
    new_clip = clip.fx(vfx.speedx, clip_duration / duration)
    return new_clip
