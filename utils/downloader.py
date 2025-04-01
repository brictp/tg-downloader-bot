import yt_dlp
import os


def download_video(url):
    options = {
        "outtmpl": "./media/%(title)s.%(ext)s",
        "format": "mp4/bestvideo[filesize<20M]+bestaudio/best",  # Intenta elegir calidad < 20MB
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        ruta_video = ydl.prepare_filename(info)

    # Verificar tamaño del archivo
    if os.path.exists(ruta_video):
        file_size = os.path.getsize(ruta_video) / (1024 * 1024)  # Convertir a MB
        if file_size > 20:
            os.remove(ruta_video)  # Borrar archivo si excede el límite
            return "Archivo demasiado grande, se ha eliminado."

    return ruta_video
