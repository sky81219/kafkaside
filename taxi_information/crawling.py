import os
import pathlib
import collections
import calendar
import logger

from typing import List
from queue import Queue

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from seleniumUtil import GoogleUtilityDriver as gd


if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable


try:
    os.mkdir(f"{pathlib.Path().cwd()}/data/")
except FileExistsError:
    print(f'An error has occurred. Continuing anyway')


q = Queue()
log = logger.log()
month = list(calendar.month_name)
tlc_url = gd().page()


def dd(element: BeautifulSoup) -> List[str]:
    return [data["href"] for data in element.find_all("a", {"title": "For-Hire Vehicle Trip Records"})]


def fd(element: BeautifulSoup) -> None:
    for i in element.find_all("p"):
        try:
            if month.index(i.text): 
                os.mkdir(f"{pathlib.Path().cwd()}/data/{month.index(i.text)}/")
        except (FileExistsError, ValueError):
            continue 

        
def search_injection() -> None:
    bs = BeautifulSoup(tlc_url, "html.parser")
    for i in range(22, 19, -1):
        for inner in bs.find_all("div", {"class": "faq-answers", "id": f"faq20{i}"}): 
            fd(inner)
            data_struct = dd(inner)
            q.put(data_struct)


def download() -> None:
    j = 0
    while j < 3:
        for da in q.get():
            name: str = da.split("/")[4]
            name_number = int(name.split("_")[2].split("-")[1].split(".")[0])
            file_location = f'{os.getcwd()}/data/{name_number}/{name}'
            log.info(f"{file_location}/{name_number} 파일로 저장합니다")
            urlretrieve(da, file_location)
        j+=1     

  
search_injection()
download()