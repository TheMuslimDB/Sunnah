import requests
import json
from bs4 import BeautifulSoup

SITE_URL = "https://sunnah.com"
SITE = "sunnah.com"

def scarpe_Forty_Hadith_of_an_Nawawi():
    FILE_NAME = "Forty_Hadith_of_an-Nawawi"
    SAVE_JSON = True
    SAVE_HTML = True

    res = requests.get("https://sunnah.com/nawawi40")
    # save html site 
    if res.status_code == 200:
        if SAVE_HTML:
            with open(f"{FILE_NAME}.html","w") as f:
                f.write(res.text)
    else: 
        print("Failed to connect to website")
        return
    

    soup = BeautifulSoup(res.text,features="lxml")
    containers = soup.select(".actualHadithContainer")



    hadith_info = {
        "additional" : {
            "intro": {
                "langs": {
                    "arabic": soup.select(".arabic.abookintro p")[0].text,
                    "english":  soup.select(".ebookintro p")[0].text,
                }
            }
        },
        "hadiths" : []
    }
    for container in containers:
        arabic_text = container.select(".arabic_hadith_full")[0].text
        arabic_source = {}
        for source in container.select(".arabic_hadith_full a"):
            href = source["href"] if SITE in source["href"] else SITE_URL + source["href"]   
            arabic_source[source.text] = href 

        english_text = container.select(".english_hadith_full")[0].text
        english_source = {}
        for source in container.select(".english_hadith_full a"):
            href = source["href"] if SITE in source["href"] else SITE_URL + source["href"]   
            english_source[source.text] = href 

        ref = SITE_URL + container.select(".hadith_reference a")[0]["href"]

        hadith_info["hadiths"].append({
            "ref" : ref,
            "langs" : {
                "arabic": {
                    "text": arabic_text,
                    "source" : arabic_source,
                },
                "english": {
                    "text": english_text,
                    "source" : english_source,
                },
            },
        })

    if SAVE_JSON:
        with open(f"{FILE_NAME}.json","w") as f:
            json.dump(hadith_info,f)


scarpe_Forty_Hadith_of_an_Nawawi()