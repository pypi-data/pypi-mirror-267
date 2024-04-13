import time, aiohttp, asyncio
from aioxdl.scripts import Scripted
from yt_dlp import YoutubeDL, DownloadError
from aioxdl.functions import Hkeys, EXlogger
#=================================================================================================

class Downloader:

    def __init__(self, message=None):
        self.tsize = 0
        self.dsize = 0
        self.stime = 0
        self.error = None
        self.chunk = 1024
        self.imssg = message
        self.etime = Scripted.DATA01
        self.comnd = {"quiet": True,  "no_warnings": True, "logger": EXlogger()}

#=================================================================================================

    async def filename(self, filelink):
        with YoutubeDL(self.comnd) as ydl:
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
        await progress(self.imssg, self.stime, self.tsize, self.dsize) if progress else None

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

                await response.release()
                return location if location else None

#=================================================================================================

    async def start(self, url, flocations, timeout=1000, progress=None):
        try:
            self.stime = time.time()
            flocations = await self.download(url, flocations, timeout, progress)
        except aiohttp.ClientConnectorError as errors:
            self.error = errors
        except asyncio.TimeoutError:
            self.error = self.etime
        except Exception as errors:
            self.error = errors

        return flocations

#=================================================================================================
                       
