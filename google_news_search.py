import os
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from datetime import datetime
import requests


# Simple definition of encoding for each language
def select_encoding(lang):
    if lang in ["CZ", "HR", "EN", "DE", "HU", "PL", "SK", "SI", "RO"]:
        return "windows-1250"
    elif lang in ["BG"]:
        return "windows-1251"
    elif lang in ["DA", "NL", "FR", "FI", "GA", "pt-PT", "IT", "ES", "SV", "MT"]:
        return "windows-1252"
    elif lang in ["EL"]:
        return "windows-1253"
    elif lang in ["ET", "LT", "LV"]:
        return "windows-1257"
    elif lang in []:
        return ""

# Get sector based on order


def get_sector(q_id):
    if q_id == 0:
        return "AG_AC"
    elif q_id == 1:
        return "AG_PC"
    elif q_id == 2:
        return "AG_LS"
    elif q_id == 3:
        return "EC_AQ"
    elif q_id == 4:
        return "EC_TR"
    elif q_id == 5:
        return "EN_HY"
    elif q_id == 6:
        return "EN_TH"
    elif q_id == 7:
        return "IN_TR"
    elif q_id == 8:
        return "PU_WS"
    else:
        return "_"


# Select search geographical domain based on language
def get_rss_url(language):
    if language == "BG":
        return "https://news.google.com/rss/search?hl=bg&gl=bg&ceid=BG:bg&"
    elif language == "CZ":
        return "https://news.google.com/rss/search?hl=cs&gl=cz&ceid=CZ:cs&"
    elif language == "DA":
        return "https://news.google.com/rss/search?hl=da&gl=cz&ceid=DK:da&"
    elif language == "DE":
        return "https://news.google.com/rss/search?hl=de&gl=de&ceid=DE:de&"
    elif language == "EN":
        return "https://news.google.com/rss/search?hl=en&gl=en&ceid=EN:en&"
    elif language == "EL":
        return "https://news.google.com/rss/search?hl=el&gl=gr&ceid=GR:el&"
    elif language == "ES":
        return "https://news.google.com/rss/search?hl=es&gl=es&ceid=ES:es&"
    elif language == "ET":
        return "https://news.google.com/rss/search?hl=et&gl=ee&ceid=EE:et&"
    elif language == "FI":
        return "https://news.google.com/rss/search?hl=fi&gl=fi&ceid=FI:fi&"
    elif language == "FR":
        return "https://news.google.com/rss/search?hl=fr&gl=fr&ceid=FR:fr&"
    elif language == "GA":
        return "https://news.google.com/rss/search?hl=ga&gl=ie&ceid=IE:ga&"
    elif language == "HR":
        return "https://news.google.com/rss/search?hl=hr&gl=hr&ceid=HR:hr&"
    elif language == "HU":
        return "https://news.google.com/rss/search?hl=hu&gl=hu&ceid=HU:hu&"
    elif language == "IT":
        return "https://news.google.com/rss/search?hl=it&gl=it&ceid=IT:it&"
    elif language == "LT":
        return "https://news.google.com/rss/search?hl=lt&gl=lt&ceid=LT:lt&"
    elif language == "LV":
        return "https://news.google.com/rss/search?hl=lv&gl=lv&ceid=LV:lv&"
    elif language == "MT":
        return "https://news.google.com/rss/search?hl=mt&gl=mt&ceid=MT:mt&"
    elif language == "NL":
        return "https://news.google.com/rss/search?hl=nl&gl=nl&ceid=NL:nl&"
    elif language == "PL":
        return "https://news.google.com/rss/search?hl=pl&gl=pl&ceid=PL:pl&"
    elif language == "pt-PT":
        return "https://news.google.com/rss/search?hl=pt-PT&gl=pt&ceid=PT:pt-PT&"
    elif language == "RO":
        return "https://news.google.com/rss/search?hl=ro&gl=ro&ceid=RO:ro&"
    elif language == "SI":
        return "https://news.google.com/rss/search?hl=si&gl=si&ceid=SI:si&"
    elif language == "SK":
        return "https://news.google.com/rss/search?hl=sk&gl=sk&ceid=SK:sk&"
    elif language == "SV":
        return "https://news.google.com/rss/search?hl=sv&gl=se&ceid=SE:sv&"
    else:
        return "_"


def get_news_articles(q, date, lang='EN') -> list:
    link = get_rss_url(lang)
    query = urlencode({"q": q})
    url = link + query

    # Make request
    resp = requests.get(url)
    content = resp.text
    tree = ET.fromstring(content)

    rows = []

    # Parse XML output
    for item in tree.findall(".//item"):
        element_content = list(item)
        publish_date = element_content[3].text
        publish_date_object = datetime.strptime(
            publish_date, "%a, %d %b %Y %H:%M:%S GMT"
        ).date()
        if publish_date_object >= date:
            title = element_content[0].text
            link = element_content[1].text
            source = element_content[5].text
            append_row = [title, link, publish_date, source]
            rows.append(append_row)

    return rows
