from faster_whisper import WhisperModel



model = WhisperModel("medium")


def transcribe_audio(audio_stream):
    segments, _ = model.transcribe(audio_stream)
    user_text = " ".join([seg.text for seg in segments])
    return user_text