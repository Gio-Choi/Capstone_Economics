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

# # 네이버 금융 재무제표 크롤러
#
# 종목코드를 리스트로 넣으면 재무제표를 데이터프레임으로 받아오고, 엑셀로 만들어준다.

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

codes = ['002840', '107590', '134380', '003650', '084990', '052260', '003610', '001340', '014580', '035150', '002410', '007210', '002760', '003850', '032350',
 '000400', '023530', '004990', '005300', '011170', '002270', '071840', '038060', '058470', '014470', '027740', '001080', '005990', '072870', '086900', '078160',
 '138040', '008560', '000060', '017180', '012690', '005360', '080160', '009680', '009580', '009200', '033920', '008420', '025560', '007120', '000020', '000150',
 '082740', '042670', '034020', '024090', '003160', '092200', '090710', '013570', '026890', '115390']

# +
URL = "https://finance.naver.com/item/main.nhn?code=001040" 

samsung_electronic = requests.get(URL)
html = samsung_electronic.text
soup = BeautifulSoup(html, 'html.parser')
finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]
th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
annual_date = th_data[3:7]   
finance_index = ['001040'] 
finance_data = [item.get_text().strip() for item in finance_html.select('td')]
finance_data = np.array(finance_data)
finance_data.resize(len(finance_index), 4)
finance_date = annual_date
df1 = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)
# -

df1



# +
#빈 데이터 프레임 하나 만들고 for문으로 하나씩 행추가하기 !!
## 위에꺼 따라 일단 첫번째 code는 for문에서 빼서 데이터프레임 하나 만든 후에(전역변수로), concat()함수로 하나씩 채워나가자 !
for code in codes :
    
    if code == '002840':
        URL = "https://finance.naver.com/item/main.nhn?code=007120"
    
        samsung_electronic = requests.get(URL)
        html = samsung_electronic.text        
        soup = BeautifulSoup(html, 'html.parser')
        finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]
        th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
        annual_date = th_data[3:7]   
        finance_index = ['007120'] 
        finance_data = [item.get_text().strip() for item in finance_html.select('td')]
        finance_data = np.array(finance_data)
        finance_data.resize(len(finance_index), 4)
        finance_date = annual_date
        df1 = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)

        URL = "https://finance.naver.com/item/main.nhn?code=" + code
    
        samsung_electronic = requests.get(URL)
        html = samsung_electronic.text        
        soup = BeautifulSoup(html, 'html.parser')
        finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]
        th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
        annual_date = th_data[3:7]   
        finance_index = [code] 
        finance_data = [item.get_text().strip() for item in finance_html.select('td')]
        finance_data = np.array(finance_data)
        finance_data.resize(len(finance_index), 4)
        finance_date = annual_date
        df2 = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)
    
        df1 = pd.concat([df1,df2])
    
    
    else :
        URL = "https://finance.naver.com/item/main.nhn?code=" + code
    
        samsung_electronic = requests.get(URL)
        html = samsung_electronic.text        
        soup = BeautifulSoup(html, 'html.parser')
        finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]
        th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
        annual_date = th_data[3:7]   
        finance_index = [code] 
        finance_data = [item.get_text().strip() for item in finance_html.select('td')]
        finance_data = np.array(finance_data)
        finance_data.resize(len(finance_index), 4)
        finance_date = annual_date
        df2 = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)
    
        df1 = pd.concat([df1,df2])
    
        df1.to_excel('test.xlsx')
        


# -

# ## End

    th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
     annual_date = th_data[3:7]
#quarter_date = th_data[7:13]

    annual_date

# +
    finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:4] 

##여기다가 매출액말고 회사명을 넣으면 쫘악 정리가 될 듯 !!!

# -

    finance_index

    finance_data = [item.get_text().strip() for item in finance_html.select('td')]


    finance_data = np.array(finance_data)
    finance_data.resize(len(finance_index), 4)

    finance_data

    finance_date = annual_date 
    finance_date


     

    finance = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)








# +
    finance.to_excel('test.xlsx')

##   1) 따로 엑셀을 만든 후에 파일명에다가 회사명을 넣어도 좋을 듯 !! 2) 아니면 한번에 데이터프레임을 만들어서 합치는 것도 좋을 듯 !!  
# -


