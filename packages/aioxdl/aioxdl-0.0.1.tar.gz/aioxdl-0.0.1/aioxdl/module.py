import time, aiohttp
#=======================================================================================================

class Downloader:

    def __init__(self, imsg=None):
        self.tsize = 0
        self.dsize = 0
        self.chunk = 1024
        self.timeo = 1000
        self.imesg = imsg
        self.stime = time.time()

#=======================================================================================================

    async def getsizes(self, response):
        return int(response.headers.get("Content-Length", 0)) or 0

    async def checkurl(self, url, timeout=20):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                return 200 if response.status == 200 else response.status

    async def display(self, progress):
        await progress(self.imesg, self.stime, self.tsize, self.dsize) if progress else None

#=======================================================================================================

    async def downadl(self, url, location, timeout, progress):
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
                        await self.display(progress)

                return location

#=======================================================================================================

    async def download(self, url, location, timeout=1000, progress=None):
        try:
            messages = None
            location = await self.downadl(url, location, timeout, progress)
        except Exception as errors:
            messages = errors
        
        return messages, location

#=======================================================================================================
                       
