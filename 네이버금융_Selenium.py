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
    

company_list = ['002840', '107590', '134380', '003650', '084990', '052260', '003610', '001340', '014580', '035150',]


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
    
    #기업명 뽑기
    title0 = html1.find('head').find('title').text
    print(title0.split('-')[-1])
    
    html22 = html1.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})
    
    #date scrapy
    thead0 = html22.find('thead')
    tr0 = thead0.find_all('tr')[1]
    th0 = tr0.find_all('th')
    
    date = []
    for i in range(len(th0)):
        date.append(''.join(re.findall('[0-9/]',th0[i].text)))
    
    #columns scrapy
    tbody0 = html22.find('tbody')
    tr0 = tbody0.find_all('tr')
    
    col = []
    for i in range(len(tr0)):

        if '\xa0' in tr0[i].find('th').text:
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
    
    multiple_index = []    # 빈 리스트 생성
 
    for i in range(len(date)):
      
        multiple_index.append(code)
    
    
    
    ####
    df = pd.DataFrame(td2,columns = col,index = [multiple_index, date])
    
    ###5번째 행까지만 살리기
    df.drop(df.index[5:], inplace=True)
    time.sleep(1)
    
    
    return df

df_first_row = stock_crawler('005930')

df_first_row

for i in company_list :
    df_new = stock_crawler(i)
    df_first_row = pd.concat([df_first_row, df_new])
    
    
    
    ##
    if i == company_list[5] :
        df_first_row.to_excel('tobinq.xlsx')
        time.sleep(3)
        
    
    ##
    

df_all = df_first_row
df_all.to_excel('tobinq.xlsx')


