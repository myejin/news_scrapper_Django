import requests
from bs4 import BeautifulSoup
from pprint import pprint

url_list = []
try:
    for num in range(1, 100, 10):
        resp = requests.get(
            f"https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=lg%20%ED%99%94%ED%95%99&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0140004734048&nso=so:r,p:all,a:all&start={num}"
        ).text
        html = BeautifulSoup(resp, "html.parser")

        for i in range(10):
            url = html.select_one(f"#sp_rns{num + i} > div > div > a").attrs["href"]
            url_list.append(url)

except Exception:
    print("finish")

pprint(url_list)
