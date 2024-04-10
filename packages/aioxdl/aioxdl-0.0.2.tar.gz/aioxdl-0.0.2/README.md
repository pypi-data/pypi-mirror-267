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
	percentage = (dsize / tsize) * 100
	print("{}%".format(round(percentage), 2))

async def main():
    core = Downloader()
    file = "testfile.mkv"
    link = "https://www.tg-x.workers.dev/dl/18357?hash=AgADIh"
    ou, _ = await core.start(link, file, progress=progress)
    print(ou)

asyncio.run(main())
```
