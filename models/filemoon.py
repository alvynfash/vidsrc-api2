from .utils import fetch
import re
import requests
from .decoders.packed import *
from . import subtitle
async def handle(url) -> dict:
    print('Filemoon handle')
    URL = url.split("?")
    SRC_URL = URL[0]
    SUB_URL = URL[1]

    # GET SUB
    subtitles = []
    subtitles = await subtitle.vscsubs(SUB_URL)

	# GET SRC
    # request = await fetch(SRC_URL)
    key= 'scp-live-9bc4c7e194dd4a19b92213ce243f8243'
    url = f"https://api.scrapfly.io/scrape?tags=player%2Cproject%3Adefault&asp=true&render_js=true&key={key}&url={SRC_URL}"
    request = requests.request("GET", url)
    content = request.json()['result']['content']
    # content = request.text
    processed_matches = await process_packed_args(content)
    unpacked = await unpack(*processed_matches)
    hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)
    return {
        'stream':hls_url,
        'subtitle':subtitles,
	'filemoon':SRC_URL
    }
