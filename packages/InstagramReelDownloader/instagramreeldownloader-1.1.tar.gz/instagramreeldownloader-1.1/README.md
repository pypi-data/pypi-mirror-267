# Instagram Reel Downloader

## Overview
This project aims to build a headless Instagram reel downloader using Selenium WebDriver.

[//]: # ()
[//]: # (## Download stats)

[//]: # ([![Downloads]&#40;https://static.pepy.tech/badge/ActiveCollab&#41;]&#40;https://pepy.tech/project/ActiveCollab&#41; <br>)

[//]: # ([![Downloads]&#40;https://static.pepy.tech/badge/ActiveCollab/week&#41;]&#40;https://pepy.tech/project/ActiveCollab&#41; <br>)

[//]: # ([![Downloads]&#40;https://static.pepy.tech/badge/ActiveCollab/month&#41;]&#40;https://pepy.tech/project/ActiveCollab&#41;)


## Installation

```console
pip install InstagramReelDownloader
```
InstagramReelDownloader officially supports Python 3.8+.

## Usage

### Default
```python
from InstagramReelDownloader import ReelDownload

ReelDownload(reel_url) # url can be in any format can also pass file name else it will use "reel.mp4"
```

