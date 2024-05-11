import pdfkit
import os
from PyPDF2 import PdfMerger
import requests
from bs4 import BeautifulSoup

os.chdir(r'C:\Users\jungs\OneDrive\JungSW\011_University\021_2학년_1학기\파이썬기반응용프로그래밍\InhaChatBot\crawled_files')

options = {'quiet': ''}
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# merger = PdfMerger()

merge_list = []

for i in range(37000, 37010):
    url = f'https://www.inha.ac.kr/bbs/kr/8/{i}/artclView.do'
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")
    title = soup.find("h2", {"class":"artclViewTitle"}).get_text()
    print(title)
    if title:
        title = title + '.pdf'
        pdfkit.from_url(url, title, options=options, configuration=config)
        merge_list.append(f"crawled_files/{title}")
print(merge_list)