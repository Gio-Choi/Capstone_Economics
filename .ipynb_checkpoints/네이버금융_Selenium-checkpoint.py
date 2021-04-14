# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## 네이버금융_재무제표_크롤러
#
# '종목코드'를 입력하면 셀레늄으로 재무제표를 크롤링해오는 프로그램
# 10개 기업만 테스트로 시도해 본 결과 정상 작동함. 

import requests
from bs4 import BeautifulSoup 
from datetime import datetime                            
import pandas as pd 
import time 
import urllib.request 
from selenium.webdriver import Chrome
import json 
import re     
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt
import time


# # 기업의 '종목코드' 리스트화 해서 넣기
# 밑의 리스트는 예시

company_list = ['002840', '107590', '134380', '003650', '084990', '052260', '003610', '001340', '014580', '035150',]


# # 현재 궁금증, 고민거리
# 1)time,sleep은 몇 초 정도로 할지? 코스피, 코스닥 상장사 약 2000개 전부를 크롤링한다 생각했을 때 각 time.sleep에서 일초씩 차이가 나는 것은 총 소요시간에서 큰 차이로 이어짐. 
#
# 2)비정형 패널데이터 선형회귀 분석은 책을 한두권 사서 더 공부해보고 분석 진행. 이론이 흔들리면 안된다. 
#
# 3)왜 굳이 비정형 패널데이터 분석을 하는지? 이에 대한 소명 필요. 
#
# 4)유니코드 공백 지우기..?잘 모르겠다.. 
#
#

def stock_crawler(code):
    
    browser  = Chrome()
    browser.maximize_window()
    
    name = code
    base_url = 'https://finance.naver.com/item/coinfo.nhn?code='+ name + '&target=finsum_more'
    
    
    browser.get(base_url)
    time.sleep(2)
   
    browser.switch_to_frame(browser.find_element_by_id('coinfo_cp'))
    time.sleep(2)
    
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[3]')[0].click()
    time.sleep(2)

    html0 = browser.page_source
    html1 = BeautifulSoup(html0,'html.parser')
    
    #기업명
    title0 = html1.find('head').find('title').text
    print(title0.split('-')[-1])
    
    html22 = html1.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})
    
    #date 들고오기
    thead0 = html22.find('thead')
    tr0 = thead0.find_all('tr')[1]
    th0 = tr0.find_all('th')
    
    date = []
    for i in range(len(th0)):
        date.append(''.join(re.findall('[0-9/]',th0[i].text)))
    
    #columns 들고오기
    tbody0 = html22.find('tbody')
    tr0 = tbody0.find_all('tr')
    
    col = []
    for i in range(len(tr0)):

        if '\xa0' in tr0[i].find('th').text: #유니코드의 공백을 없애주는 방법.
            tx = re.sub('\xa0','',tr0[i].find('th').text)
        else:
            tx = tr0[i].find('th').text

        col.append(tx)
    
    #main text scrapy
    td = []
    for i in range(len(tr0)):
        td0 = tr0[i].find_all('td')
        td1 = []
        for j in range(len(td0)):
            if td0[j].text == '':
                td1.append('0')
            else:
                td1.append(td0[j].text)

        td.append(td1)
    
    td2 = list(map(list,zip(*td)))
    
    ###
    
    multiple_index = []  
 
    for i in range(len(date)):
      
        multiple_index.append(code)
    
    
    
    ####
    df = pd.DataFrame(td2,columns = col,index = [multiple_index, date])
    
    ###일단 어떤게 필요할지 몰라 다 들고왔지만 5개년, 즉 5행까지만 쓰는 걸로 잠정적 결론.
    df.drop(df.index[5:], inplace=True)
    time.sleep(1)
    
    
    return df

df_first_row = stock_crawler('005930')

df_first_row

# # for 문으로 모든 기업 크롤링 진행
#

for i in company_list :
    df_new = stock_crawler(i)
    df_first_row = pd.concat([df_first_row, df_new])
    
    
    
    ##
    if i == company_list[5] :
        df_first_row.to_excel('tobinq.xlsx')
        time.sleep(3)
        
    
    ##


#엑셀로 변환
df_all = df_first_row
df_all.to_excel('tobinq.xlsx')

# # 상의할 점
#
# 1. 기업들을 어떤 표준에 의거해서 산업 별로 분류할지? 
# 2. 캡스톤 디자인 예산 신청해서 그 돈으로 선형회귀 관련 책을 구매하는 건 가능할지?
