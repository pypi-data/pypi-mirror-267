import os, time, aiohttp, asyncio
from urllib.parse import unquote, urlparse
from yt_dlp import YoutubeDL, DownloadError
from aioxdl.functions import Hkeys, EXlogger
#=================================================================================================

class Downloader:

    def __init__(self, message=None):
        self.tsize = 0
        self.dsize = 0
        self.error = None
        self.chunk = 1024
        self.imssg = message
        self.stime = time.time()
        self.etime = "ERROR : Timeout"

#=================================================================================================

    async def filename(self, filelink):
        command = {"quiet": True,  "no_warnings": True, "logger": EXlogger()}
        with YoutubeDL(command) as ydl:
            try:
                resultse = ydl.extract_info(filelink, download=False)
                filename = ydl.prepare_filename(resultse, outtmpl=Hkeys.DATA01)
            except DownloadError:
                filename = None
            except Exception:
                filename = None

            return filename

#=================================================================================================
    
    async def getsizes(self, response):
        return int(response.headers.get("Content-Length", 0)) or 0

    async def checkurl(self, url, timeout=20):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                return 200 if response.status == 200 else response.status

    async def display(self, progress):
        await progress(self.imssg, time.time(), self.tsize, self.dsize) if progress else None

#=================================================================================================

    async def download(self, url, location, timeout, progress):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                self.tsize += await self.getsizes(response)
                with open(location, "wb") as handlexo:
                    while True:
                        chunks = await response.content.read(self.chunk)
                        if not chunks:
                            break
                        handlexo.write(chunks)
                        self.dsize += self.chunk
                        try: await self.display(progress)
                        except Exception: pass

                return location if location else None

#=================================================================================================

    async def start(self, url, location, timeout=1000, progress=None):
        try:
            location = await self.download(url, location, timeout, progress)
        except aiohttp.ClientConnectorError as errors:
            self.error = errors
        except asyncio.TimeoutError:
            self.error = self.etime
        except Exception as errors:
            self.error = errors

        return location

#=================================================================================================
                       
