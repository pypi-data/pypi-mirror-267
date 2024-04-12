<p align="center">
    📦 <a href="https://pypi.org/project/aioxdl" style="text-decoration:none;">AIO DOWNLOADER</a>
</p>

<p align="center">
   <a href="https://telegram.me/clinton_abraham"><img src="https://img.shields.io/badge/𝑪𝒍𝒊𝒏𝒕𝒐𝒏 𝑨𝒃𝒓𝒂𝒉𝒂𝒎-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/Space_x_bots"><img src="https://img.shields.io/badge/Sᴘᴀᴄᴇ ✗ ʙᴏᴛꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/sources_codes"><img src="https://img.shields.io/badge/Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
</p>

## INSTALLATION
```bash
pip install aioxdl
```

## USAGE

```python
import time, asyncio
from aioxdl import Downloader

async def progress(_, stime, tsize, dsize):
    percentage = round((dsize / tsize) * 100, 2)
    print("COMPLETED : {}%".format(percentage))

async def main():
    core = Downloader()
    loca = "./Downloads/testfile.mkv"
    link = "https://www.tg-x.workers.dev/dl/18357?hash=AgADIh"
    file = await core.start(link, loca, progress=progress)
    fine = file if core.error == None else core.error
    print(fine)

asyncio.run(main())

#===[ PROGRESS FUNCTION ]===

# stime = start time
# tsize = total size
# dsize = download size

```
