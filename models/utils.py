import httpx,base64,ssl,certifi
from fastapi import HTTPException
from urllib.parse import unquote
import requests

BASE = 'http://localhost:8000'
session = requests.Session()

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
    # # context = ssl.create_default_context()
    # # context.load_verify_locations(certifi.where())
    # async with httpx.AsyncClient(follow_redirects=redirects, verify=context) as client:
    #     headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    #     headers["content-type"]= "application/json"
    #     headers["access-control-allow-origin"]= "*"
    #     headers["access-control-allow-headers"]= "Content-Type,Authorization"
    #     headers["access-control-allow-methods"]= "GET,POST,PUT,DELETE,OPTIONS"
    #     headers["access-control-expose-headers"]= "*"
    #     print(f"Fetching: {url}")
    #     print(f"Headers: {headers}")
    #     if method=="GET":
    #         # response = await client.get(url,headers=headers)
    #         response= session.get(url, headers=headers)
    #         return response
    #     if method=="POST":
    #         response = await client.post(url,headers=headers,data=data)
    #         return response
    #     else:
    #         return "ERROR"
    
    print(f"Fetching: {url}")

    # headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    # headers["content-type"]= "application/json"
    # headers["access-control-allow-origin"]= "*"
    # headers["access-control-allow-headers"]= "Content-Type,Authorization"
    # headers["access-control-allow-methods"]= "GET,POST,PUT,DELETE,OPTIONS"
    # headers["access-control-expose-headers"]= "*"
    # headers["Origin"]= "https://vidsrc.me"
    # session.headers.update(headers)

    # proxies= {"http://2.56.119.93:5074",}

    if method=="GET":
        response= session.get(url, headers=headers, allow_redirects=True, debug=True)
        print("Response: ",response)
        return response
    if method=="POST":
        response = await session.post(url,headers=headers,data=data)
        print("Response: ",response)
        return response
    else:
        return "ERROR"
