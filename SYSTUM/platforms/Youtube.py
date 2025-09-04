import asyncio
from typing import Union
import httpx

API_URL = "https://api.thequickearn.xyz"
VIDEO_API_URL = "https://api.video.thequickearn.xyz"
API_KEY = "30DxNexGenBots121b50"

class YouTubeAPI:
    def __init__(self):
        self.api_headers = {"Authorization": f"Bearer {API_KEY}"}

    # ----------------- Video Details -----------------
    async def details(self, video_id: str):
        """Fetch full video details"""
        url = f"{VIDEO_API_URL}/details/{video_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.api_headers)
            if resp.status_code != 200:
                return None
            data = resp.json()
            return (
                data.get("title"),
                data.get("duration"),
                data.get("duration_sec"),
                data.get("thumbnail"),
                data.get("id")
            )

    async def title(self, video_id: str):
        details = await self.details(video_id)
        return details[0] if details else None

    async def duration(self, video_id: str):
        details = await self.details(video_id)
        return details[1] if details else None

    async def thumbnail(self, video_id: str):
        details = await self.details(video_id)
        return details[3] if details else None

    # ----------------- Download -----------------
    async def download(self, video_id: str, quality: str = "720p", audio_only: bool = False):
        """Get download link from API"""
        url = f"{VIDEO_API_URL}/download/{video_id}"
        params = {"quality": quality, "audio_only": audio_only}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.api_headers, params=params)
            if resp.status_code != 200:
                return None
            return resp.json().get("download_url")

    # ----------------- Playlist -----------------
    async def playlist(self, playlist_id: str, limit: int = 10):
        url = f"{VIDEO_API_URL}/playlist/{playlist_id}"
        params = {"limit": limit}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.api_headers, params=params)
            if resp.status_code != 200:
                return []
            return resp.json().get("videos", [])

    # ----------------- Search -----------------
    async def search(self, query: str, limit: int = 5):
        url = f"{API_URL}/search"
        params = {"query": query, "limit": limit}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.api_headers, params=params)
            if resp.status_code != 200:
                return []
            return resp.json().get("results", [])

    # ----------------- Formats -----------------
    async def formats(self, video_id: str):
        """Get available formats"""
        url = f"{VIDEO_API_URL}/formats/{video_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.api_headers)
            if resp.status_code != 200:
                return []
            return resp.json().get("formats", [])

    # ----------------- Track -----------------
    async def track(self, video_id: str):
        """Return track details like title, link, duration, thumbnail"""
        details = await self.details(video_id)
        if not details:
            return None, None
        track_details = {
            "title": details[0],
            "link": f"https://youtu.be/{details[4]}",
            "vidid": details[4],
            "duration_min": details[1],
            "thumb": details[3],
        }
        return track_details, details[4]

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True, "cookiefile" : cookie_txt_file()}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except:
                    continue
                if not "dash" in str(format["format"]).lower():
                    try:
                        format["format"]
                        format["filesize"]
                        format["format_id"]
                        format["ext"]
                        format["format_note"]
                    except:
                        continue
                    formats_available.append(
                        {
                            "format": format["format"],
                            "filesize": format["filesize"],
                            "format_id": format["format_id"],
                            "ext": format["ext"],
                            "format_note": format["format_note"],
                            "yturl": link,
                        }
                    )
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()
        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile" : cookie_txt_file(),
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "cookiefile" : cookie_txt_file(),
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_video_dl():
            formats = f"{format_id}+140"
            fpath = f"downloads/{title}"
            ydl_optssx = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile" : cookie_txt_file(),
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_optssx = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile" : cookie_txt_file(),
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        if songvideo:
            await loop.run_in_executor(None, song_video_dl)
            fpath = f"downloads/{title}.mp4"
            return fpath
        elif songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            fpath = f"downloads/{title}.mp3"
            return fpath
        elif video:
            if await is_on_off(1):
                direct = True
                downloaded_file = await loop.run_in_executor(None, video_dl)
            else:
                proc = await asyncio.create_subprocess_exec(
                    "yt-dlp",
                    "--cookies",cookie_txt_file(),
                    "-g",
                    "-f",
                    "best[height<=?720][width<=?1280]",
                    f"{link}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = False
                else:
                   file_size = await check_file_size(link)
                   if not file_size:
                     print("None file Size")
                     return
                   total_size_mb = file_size / (1024 * 1024)
                   if total_size_mb > 250:
                     print(f"File size {total_size_mb:.2f} MB exceeds the 100MB limit.")
                     return None
                   direct = True
                   downloaded_file = await loop.run_in_executor(None, video_dl)
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, direct
