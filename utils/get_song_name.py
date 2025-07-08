import os
import base64
import requests
from pydub import AudioSegment

from utils import register_error
from config import SHAZAM_API_TOKEN


async def identify_song_from_file(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        return "Error finding path"

    try:
        audio = AudioSegment.from_wav(audio_path)
        short_audio = audio[:5000]  # ~5 segundos

        short_audio = (
            short_audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
        )

        # Exportar a datos RAW PCM
        raw_bytes = short_audio.raw_data
        size_kb = len(raw_bytes) / 1024
        if size_kb > 500:
            return "Error audio too large to shazam"

        # Codifica en Base64
        audio_b64 = base64.b64encode(raw_bytes).decode("utf-8")

        # Solicitud a la API
        url = "https://shazam.p.rapidapi.com/songs/v2/detect"
        headers = {
            "x-rapidapi-key": SHAZAM_API_TOKEN,
            "x-rapidapi-host": "shazam.p.rapidapi.com",
            "Content-Type": "text/plain",
        }
        querystring = {"timezone": "America/Chicago", "locale": "en-US"}

        response = requests.post(
            url, data=audio_b64, headers=headers, params=querystring
        )

        res = response.json()

        track = res.get("track")
        if track:
            title = track.get("title")
            artist = track.get("subtitle")
            return f"{title} - {artist}"
        else:
            return "Cant get song name"

    except Exception as e:
        register_error(f"Error al obtener el nombre de la canción: {e}")
        return "Error al obtener el nombre de la canción."
