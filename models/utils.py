import httpx,base64,ssl,certifi
from fastapi import HTTPException
from urllib.parse import unquote
import requests

BASE = 'http://localhost:8000'
# session = requests.Session()

async def default():
    return ''

async def error(err:str):
    # TODO
    #    return {
    #        "status":500,
    #        "info":err,
    #        "sources":[]
    #    }
    print(err) # for understanding whats gone wrong in the deployment.viewable in vercel logs.
    return {}
async def decode_url(encrypted_source_url:str,VIDSRC_KEY:str):
    standardized_input = encrypted_source_url.replace('_', '/').replace('-', '+')
    binary_data = base64.b64decode(standardized_input)
    encoded = bytearray(binary_data)
    key_bytes = bytes(VIDSRC_KEY, 'utf-8')
    j = 0
    s = bytearray(range(256))

    for i in range(256):
      j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
      s[i], s[j] = s[j], s[i]

    decoded = bytearray(len(encoded))
    i = 0
    k = 0
    for index in range(len(encoded)):
      i = (i + 1) & 0xff
      k = (k + s[i]) & 0xff
      s[i], s[k] = s[k], s[i]
      t = (s[i] + s[k]) & 0xff
      decoded[index] = encoded[index] ^ s[t]
    decoded_text = decoded.decode('utf-8')
    return unquote(decoded_text)

async def fetch(url:str,headers:dict={},method:str="GET",data=None,redirects:bool=True):
    print(f"Fetching: {url}")

    async with httpx.AsyncClient(follow_redirects=redirects) as client:
        headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        # cookies={"cf_clearance":"32xoEPSuDPXhdAPfCmau9P3MGnRfXD9_Cs83iEDXWrc-1720956533-1.0.1.1-IY.xEewBEyQ2WLVZHPvephKof6HfFD8LoOGcQrBZEsXW9J9nuNMcyUsGXoku7fgAY_fuECECCJkmztH5nX3Sng"},
        if method=="GET":
            response = await client.get(url, headers=headers, follow_redirects=redirects)
            print("Response: ",response)
            return response
        if method=="POST":
            response = await client.post(url,headers=headers,data=data, follow_redirects=redirects)
            print("Response: ",response)
            return response
        else:
            return "ERROR"
