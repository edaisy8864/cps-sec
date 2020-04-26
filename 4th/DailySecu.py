'''
작성자 : 20184601 정가원

이 프로그램은 보안 전문 뉴스 <데일리시큐> 에서
'코로나'라는 키워드로 검색된 목록을
웹 크롤링 한 것입니다.
'''

import requests
from bs4 import BeautifulSoup
import csv

class NewsScraper() :

    def __init__(self) :
        self.url = 'https://www.dailysecu.com/news/articleList.html?&total=76&box_idxno=&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=%EC%BD%94%EB%A1%9C%EB%82%98&sc_multi_code=&sc_is_image=&sc_is_movie=&sc_order_by=E'
        #현재 url에는 페이지와 관련한 문자(&page=)는 임의로 지워진 상태

    def getHTML(self, cnt) :
        res = requests.get(self.url + "&page=" + str(cnt))  # 여기서 페이지와 관련된 url 정하기

        if res.status_code != 200 :
            print("request error : ", res.status_code)
        
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def getPages(self, soup) :
        pages = soup.select(".pagination > li > a")
        return len(pages)-2     # 맨처음으로 화살표와 맨끝으로 화살표가 a클래스에 포함되어 카운트 되었으므로 제외.

    def getNews(self, soup, cnt) :
        title = soup.find_all(class_ = 'links')
        date = soup.find_all(class_ = 'list-dated')

        newsTitle = []  #뉴스의 제목
        newsLink = []   #뉴스의 상세보기 링크
        newsDate = []   #기자, 작성날짜 및 시간
        
        for i in title:
            newsTitle.append(i.text)
            newsLink.append("https://www.dailysecu.com" + i.attrs['href'])
    
        for j in date:
            newsDate.append(j.text)

        for k in range(len(newsTitle)-1): # 사이트 대표링크가 하나 포함되어 있으므로 하나 제외
            print("\n" + newsTitle[k])
            print(newsLink[k])
            print(newsDate[k])
            

        self.writeCSV(newsTitle, newsLink, newsDate, cnt)


    def writeCSV (self, Title, Link, Date, cnt) :
        file = open('DailySecu.csv','a', newline='')
        wr = csv.writer(file)

        for i in range(len(Title)-1):                                        
            wr.writerow([str((cnt-1) *20 + i + 1 ), Title[i], Link[i], Date[i]])
        
        file.close()


    def scrap(self) :

        soupPage = self.getHTML(1)
        pages = self.getPages(soupPage)

        file = open('DailySecu.csv','w', newline='')
        wr = csv.writer(file)
        wr.writerow(['no.', 'Title', 'Link', 'Date'])

        file.close()
        
        for i in range(pages) :
            soupCard = self.getHTML(i+1)
            self.getNews(soupCard, i+1)
            print(i+1, "page Done\n")
        
if __name__ == "__main__":
    newsScraper = NewsScraper()
    newsScraper.scrap()