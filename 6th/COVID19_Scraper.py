'''
작성자 : 20184601 정가원

이 프로그램은 코로나바이러스감염증-19 정식 홈페이지에서
카테고리 뉴스&이슈 보도자료에서
'카드뉴스'라는 키워드로 검색된 목록을
웹 크롤링 한 것입니다.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/6th/chromedriver"
driver = webdriver.Chrome(path)

try:
    driver.get("http://ncov.mohw.go.kr/tcmBoardList.do?brdId=&brdGubun=&dataGubun=&ncvContSeq=&contSeq=&board_id=&gubun=")
    time.sleep(1)

    searchIndex = "카드뉴스"
    element = driver.find_element_by_id("search_content")
    element.send_keys(searchIndex)
    driver.find_element_by_class_name("btn_gray").click()

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    pages = (int)(bs.find("a", class_ = "p_last").attrs["onclick"].split("(")[1].split(")")[0])
    checkpages = 10     #다음으로 넘어가기전 페이지가 기본적으로 10개씩 설정되어있음.
        
    for j in range((int)((pages/10)+0.9)) :  # 10페이지씩 나오므로 전체페이지에서 10페이지를 나눈 값에 0.9를 더한 결과(소숫점 올림을 위해)의 정수부분 만큼 반복
            
        if j == ((int)((pages/10)+0.9))-1:  # 만약 반복의 마지막이라면
            checkpages = pages%10   # 확인해야할 페이지를 10으로 나눈 나머지로 변경

        for i in range(checkpages) :
            time.sleep(1)
            html = driver.page_source
            bs = BeautifulSoup(html, "html.parser")

            conts = bs.find_all("td", class_ = "ta_l")

            print("\n\n" + str(j*10+i+1) + "페이지\n")
            for c in conts :
                print(c.find("a", class_ = "bl_link").text)

            driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/a[' + str(i+3) + ']').click()

finally:
    time.sleep(3)
    driver.quit()
