import requests
import json
from bs4 import BeautifulSoup

SITE_URL = "https://sunnah.com"
SITE = "sunnah.com"

def scarpe_forty_hadith_of_an_nawawi():
    FILE_NAME = "Forty_Hadith_Of_An_Nawawi"
    SAVE_JSON = True
    SAVE_HTML = True

    res = requests.get("https://sunnah.com/nawawi40")
    # save html site 
    if res.status_code == 200:
        if SAVE_HTML:
            with open(f"output/{FILE_NAME}.html","w") as f:
                f.write(res.text)
    else: 
        print("Failed to connect to website")
        return
    

    soup = BeautifulSoup(res.text,features="lxml")
    containers = soup.select(".actualHadithContainer")


    hadith_info = {
        "intro": {
            "langs": {
                "arabic": soup.select(".arabic.abookintro p")[0].text,
                "english":  soup.select(".ebookintro p")[0].text,
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
        with open(f"output/{FILE_NAME}.json","w") as f:
            json.dump(hadith_info,f)

def scarpe_riyad_as_salihin():
    def scrape_shapter(url):
        res = requests.get(link)
        soup = BeautifulSoup(res.text,features="lxml")
        elems = soup.select(".AllHadith")[0]
        chapters = []
        chapter = {}


        for elem in elems.findChildren():
            if not elem.has_attr("class"):
                continue

            if "chapter" in elem["class"]:
                if len(chapter.keys()) != 0:
                    chapters.append(chapter)
                    chapter = {}
                chapter["title_ar"] = elem.select(".arabicchapter")[0].text
                chapter["title_en"] = elem.select(".englishchapter")[0].text
                chapter["hadiths"] = []
            elif "actualHadithContainer" in elem["class"]:
                arabic_text = elem.select(".arabic_hadith_full")[0].text
                arabic_source = {}
                for source in elem.select(".arabic_hadith_full a"):
                    href = source["href"] if SITE in source["href"] else SITE_URL + source["href"]   
                    arabic_source[source.text] = href 
                english_text = elem.select(".english_hadith_full")[0].text
                english_source = {}
                for source in elem.select(".english_hadith_full a"):
                    href = source["href"] if SITE in source["href"] else SITE_URL + source["href"]   
                    english_source[source.text] = href 
                ref = SITE_URL + elem.select(".hadith_reference a")[0]["href"]
                chapter["hadiths"].append({
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
                
        if len(chapter.keys()) != 0:
            chapters.append(chapter)
            chapter = {}

    FILE_NAME = "Riyad_As_Salihin"
    res = requests.get("https://sunnah.com/riyadussalihin")
    soup = BeautifulSoup(res.text,features="lxml")
    json_out = {
        "intro" : soup.select(".colindextitle")[1].text,
        "books": [],
    }
    json_out["books"] = []
    for title_elem in soup.select(".book_title"):
        link = SITE_URL + title_elem.select("a")[0]["href"]
        chapters = scrape_shapter(link)
        range = title_elem.select(".book_range div")
        info = {
            "title_en" :  title_elem.select(".english_book_name")[0].text,
            "title_ar" :  title_elem.select(".arabic_book_name")[0].text,
            "range": [range[0].text,range[2].text],
            "chapters": chapters,
        }
        json_out["books"].append(info)
        print(info["title_en"])
    
    with open(f"output/{FILE_NAME}.json","w") as f:
        json.dump(json_out,f)
            
def scarpe_bukhari():
    def scrape_shapter(url):
        res = requests.get(link)
        soup = BeautifulSoup(res.text,features="lxml")
        elems = soup.select(".AllHadith")[0]
        chapters = []
        chapter = {}
        try:
            for elem in elems.findChildren():
                if not elem.has_attr("class"):
                    continue

                if "chapter" in elem["class"]:
                    if len(chapter.keys()) != 0:
                        chapters.append(chapter)
                        chapter = {}
                    chapter["title_ar"] = elem.select(".arabicchapter")[0].text
                    chapter["title_en"] = elem.select(".englishchapter")[0].text
                    chapter["hadiths"] = []
                elif "actualHadithContainer" in elem["class"]:
                    arabic_text = elem.select(".arabic_hadith_full")[0].text
                    arabic_source = {}
                    for source in elem.select(".arabic_hadith_full a"):
                        href = source["href"] if SITE in source["href"] else SITE_URL + source["href"]   
                        arabic_source[source.text] = href 
                    english_text = elem.select(".english_hadith_full")[0].text
                    english_source = {}
                    for source in elem.select(".english_hadith_full a"):
                        href = source["href"] if SITE in source["href"] else SITE_URL + source["href"]   
                        english_source[source.text] = href 
                    ref = SITE_URL + elem.select(".hadith_reference a")[0]["href"]
                    chapter["hadiths"].append({
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
                    
            if len(chapter.keys()) != 0:
                chapters.append(chapter)
                chapter = {}
        except:
            print(f"Failed in {title_elem.text} {link}")        
        return chapters

    FILE_NAME = "Bukhari"
    res = requests.get("https://sunnah.com/bukhari")
    soup = BeautifulSoup(res.text,features="lxml")
    json_out = {
        "intro" : soup.select(".colindextitle")[1].text,
        "books": [],
    }
    json_out["books"] = []
    
    
    for title_elem in soup.select(".book_title"):
        link = SITE_URL + title_elem.select("a")[0]["href"]
       
        chapters = scrape_shapter(link)

        range = title_elem.select(".book_range div")
        info = {
            "title_en" :  title_elem.select(".english_book_name")[0].text,
            "title_ar" :  title_elem.select(".arabic_book_name")[0].text,
            "range": [range[0].text,range[2].text],
            "chapters": chapters,
        }
        json_out["books"].append(info)
        print(info["title_en"])
    
    with open(f"output/{FILE_NAME}.json","w") as f:
        json.dump(json_out,f)
            

# scarpe_forty_hadith_of_an_nawawi()
# scarpe_riyad_as_salihin()
# scarpe_bukhari()



            
