import base64
import requests
from pydub import AudioSegment

from utils import register_error
from config import SHAZAM_API_TOKEN


def audio_converter(audio_path: str, time_to_short: None | int) -> str:
    try:
        audio = AudioSegment.from_wav(audio_path)

        shorted_audio = (
            get_short_audio(audio, time_to_short)
            .set_frame_rate(44100)
            .set_channels(1)
            .set_sample_width(2)
        )

        # Export data to RAW PCM
        raw_bytes = shorted_audio.raw_data
        size_kb = len(raw_bytes) / 1024
        if size_kb > 500:
            return "Error audio too large to shazam"

        # Econde in Base64
        audio_b64 = base64.b64encode(raw_bytes).decode("utf-8")
        return audio_b64

    except Exception as e:
        register_error(f"Error to convert Audio {e}")
        raise ValueError("Error to convert Audio")


def get_short_audio(audio: AudioSegment, time_to_short: None | int) -> AudioSegment:
    if time_to_short is None:
        return audio[:5000]

    return audio[time_to_short : time_to_short + 5000]


def request_to_shazam(audio_b64: str) -> str:
    url = "https://shazam.p.rapidapi.com/songs/v2/detect"
    headers = {
        "x-rapidapi-key": SHAZAM_API_TOKEN,
        "x-rapidapi-host": "shazam.p.rapidapi.com",
        "Content-Type": "text/plain",
    }
    querystring = {"timezone": "America/Chicago", "locale": "en-US"}

    response = requests.post(url, data=audio_b64, headers=headers, params=querystring)

    res = response.json()
    return res


def parse_shazam_response(res: dict) -> str:
    try:
        if not isinstance(res, dict):
            return "Error: invalid response from Server"

        track = res.get("track")
        if not track:
            return "Cant find song name"

        title = track.get("title")
        artist = track.get("subtitle")

        if not title or not artist:
            return "Error incomplete song metadata"

        return f"{title} - {artist}"

    except Exception as e:
        register_error(f"Error parsing shazam response {e}")
