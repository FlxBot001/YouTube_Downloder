import yt_dlp
from celery import shared_task
from .models import Download
from django.conf import settings
import os

@shared_task
def process_download(download_id):
    download = Download.objects.get(id=download_id)
    download.status = 'processing'
    download.save()

    try:
        output_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'format': download.format_id,
            'outtmpl': os.path.join(output_dir, '%(title)s-%(format_id)s.%(ext)s'),
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(download.url, download=True)
            filename = ydl.prepare_filename(info)
            
            download.title = info.get('title', '')
            download.file_size = os.path.getsize(filename)
            download.status = 'completed'
            download.download_url = f"/media/downloads/{os.path.basename(filename)}"
            download.save()

    except Exception as e:
        download.status = 'failed'
        download.save()
        raise e