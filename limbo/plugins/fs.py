"""!calc <equation> will return the google calculator result for <equation>"""
from bs4 import BeautifulSoup
import re
try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import requests

def fs(eq):

    answer = "This is the answer to your message %s" %eq
    return answer

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"fs (.*)", text)
    if not match:
        return

    return fs(match[0].encode("utf8"))
