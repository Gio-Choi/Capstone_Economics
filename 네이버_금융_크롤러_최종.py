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

codes = ['002840',
 '107590',
 '134380',
 '003650',
 '084990',
 '052260',
 '003610',
 '001340',
 '014580',
 '035150',
 '002410',
 '007210',
 '002760',
 '003850',
 '032350',
 '000400',
 '023530',
 '004990',
 '005300',
 '011170',
 '002270',
 '071840',
 '038060',
 '058470',
 '014470',
 '027740',
 '001080',
 '005990',
 '072870',
 '086900',
 '078160',
 '138040',
 '008560',
 '000060',
 '017180',
 '012690',
 '005360',
 '080160',
 '009680',
 '009580',
 '009200',
 '033920',
 '008420',
 '025560',
 '007120',
 '000020',
 '000150',
 '082740',
 '042670',
 '034020',
 '024090',
 '003160',
 '092200',
 '090710',
 '013570',
 '026890',
 '115390']

# +
##아직 전처리 안한거

codes = [ '000890',
 '003000',
 '001270',
 '026940',
 '015350',
 '011390',
 '005030',
 '100120',
 '100220',
 '005180',
 '003960',
 '007160',
 '014710',
 '006090',
 '079660',
 '123260',
 '005090',
 '005610',
 '001470',
 '006400',
 '006660',
 '000830',
 '028260',
 '032830',
 '028050',
 '009150',
 '005930',
 '004000',
 '001360',
 '010140',
 '016360',
 '068290',
 '029780',
 '000810',
 '006110',
 '145990',
 '003230',
 '003940',
 '002170',
 '000070',
 '002810',
 '005680',
 '003720',
 '023000',
 '004380',
 '002450',
 '000520',
 '009770',
 '005500',
 '004690',
 '024950',
 '001880',
 '010960',
 '004450',
 '009470',
 '011230',
 '001820',
 '000390',
 '013700',
 '041650',
 '075180',
 '007540',
 '006730',
 '007860',
 '017390',
 '046890',
 '004410',
 '021050',
 '093920',
 '008490',
 '123420',
 '007610',
 '136490',
 '002820',
 '014620',
 '014910',
 '003080',
 '004980',
 '011300',
 '015750',
 '005980',
 '000180',
 '002420',
 '004360',
 '004490',
 '001430',
 '003030',
 '019440',
 '058650',
 '013000',
 '091090',
 '021820',
 '067830',
 '033530',
 '027970',
 '068270',
 '070300',
 '036830',
 '004430',
 '017550',
 '003060',
 '094840',
 '033170',
 '016590',
 '029530',
 '004970',
 '011930',
 '104120',
 '104110',
 '005390',
 '004170',
 '035510',
 '034300',
 '031430',
 '031440',
 '006880',
 '005800',
 '001720',
 '009270',
 '002700',
 '019170',
 '002870',
 '005450',
 '055550',
 '001770',
 '056700',
 '004080',
 '108320',
 '102280',
 '047400',
 '003410',
 '003620',
 '004770',
 '004920',
 '096530',
 '060590',
 '008700',
 '090430',
 '002790',
 '092040',
 '090370',
 '002030',
 '183190',
 '002310',
 '020560',
 '060570',
 '122900',
 '099190',
 '010780',
 '003560',
 '033660',
 '023890',
 '101140',
 '053800',
 '001780',
 '002250',
 '161000',
 '052790',
 '011090',
 '093240',
 '056190',
 '005850',
 '041510',
 '012750',
 '123700',
 '025530',
 '023960',
 '078520',
 '003800',
 '015260',
 '021080',
 '036570',
 '085310',
 '004250',
 '019590',
 '069640',
 '014440',
 '111770',
 '009970',
 '003520',
 '000670',
 '036560',
 '006740',
 '012280',
 '012160',
 '015360',
 '007310',
 '014940',
 '002630',
 '001800',
 '010470',
 '048260',
 '052770',
 '010600',
 '122870',
 '019210',
 '041190',
 '004720',
 '118000',
 '000030',
 '010050',
 '006980',
 '017370',
 '105840',
 '049800',
 '016880',
 '095720',
 '103130',
 '005820',
 '030530',
 '104830',
 '069080',
 '112040',
 '008600',
 '033270',
 '014830',
 '000910',
 '077500',
 '032620',
 '002920',
 '000700',
 '049520',
 '003470',
 '011690',
 '072130',
 '000220',
 '001200',
 '084370',
 '000100',
 '003460',
 '008730',
 '008250',
 '025820',
 '088390',
 '053350',
 '139480',
 '078020',
 '007660',
 '005950',
 '015020',
 '093230',
 '074610',
 '102460',
 '039030',
 '084680',
 '016250',
 '000760',
 '014990',
 '006490',
 '023800',
 '034590',
 '129260',
 '035080',
 '051370',
 '023810',
 '000230',
 '013360',
 '003120',
 '003200',
 '007110',
 '007570',
 '008500',
 '081000',
 '020760',
 '020150',
 '103590',
 '015860',
 '033240',
 '000950',
 '019570',
 '054950',
 '036420',
 '030000',
 '002620',
 '001560',
 '006220',
 '082270',
 '004910',
 '004700',
 '001550',
 '000480',
 '120030',
 '067000',
 '018470',
 '002600',
 '185750',
 '063160',
 '001630',
 '044380',
 '007630',
 '013870',
 '071320',
 '010580',
 '088790',
 '003780',
 '010640',
 '100250',
 '051630',
 '011000',
 '002780',
 '085660',
 '009310',
 '000650',
 '012600',
 '033250',
 '006380',
 '078340',
 '021960',
 '002380',
 '029460',
 '009070',
 '032500',
 '030200',
 '058860',
 '053210',
 '033780',
 '052400',
 '007810',
 '003690',
 '041960',
 '044820',
 '005070',
 '005420',
 '071950',
 '002020',
 '003070',
 '144620',
 '102940',
 '120110',
 '138490',
 '021240',
 '031820',
 '016600',
 '005740',
 '067280',
 '114120',
 '012170',
 '039490',
 '015890',
 '006890',
 '023160',
 '003240',
 '011280',
 '004100',
 '009410',
 '044490',
 '001420',
 '007980',
 '078000',
 '019180',
 '004870',
 '134790',
 '034230',
 '005690',
 '091700',
 '036580',
 '010820',
 '016800',
 '001020',
 '090080',
 '043370',
 '010770',
 '005490',
 '022100',
 '058430',
 '009520',
 '003670',
 '051310',
 '007330',
 '017810',
 '103140',
 '005810',
 '033180',
 '086790',
 '039130',
 '136480',
 '024660',
 '013030',
 '071090',
 '019490',
 '000080',
 '000140',
 '036460',
 '005430',
 '071050',
 '010040',
 '025540',
 '004090',
 '002200',
 '002960',
 '002000',
 '015760',
 '006200',
 '002300',
 '023350',
 '025890',
 '000970',
 '104700',
 '017960',
 '023760',
 '161890',
 '024720',
 '161390',
 '000240',
 '034830',
 '007280',
 '010100',
 '047810',
 '123690',
 '003350',
 '030520',
 '011500',
 '002390',
 '014790',
 '060980',
 '053690',
 '042700',
 '008930',
 '128940',
 '009240',
 '020000',
 '003680',
 '105630',
 '016450',
 '081970',
 '009180',
 '099660',
 '007190',
 '070590',
 '014680',
 '004710',
 '010420',
 '004150',
 '025750',
 '004960',
 '011700',
 '001750',
 '018880',
 '009420',
 '014130',
 '003300',
 '002220',
 '051600',
 '052690',
 '130660',
 '002320',
 '097230',
 '003480',
 '180640',
 '117930',
 '005110',
 '009460',
 '000880',
 '027390',
 '088350',
 '000370',
 '009830',
 '012450',
 '003530',
 '025850',
 '015540',
 '034810',
 '089470',
 '000720',
 '005440',
 '086280',
 '064350',
 '079430',
 '012330',
 '010620',
 '069960',
 '004560',
 '012630',
 '011200',
 '004310',
 '126560',
 '017800',
 '011210',
 '005380',
 '026180',
 '004020',
 '011760',
 '009540',
 '003450',
 '001450',
 '057050',
 '003010',
 '008770',
 '002460',
 '013520',
 '006060',
 '010690',
 '010660',
 '000850',
 '016580',
 '032560',
 '004800',
 '094280',
 '093370',
 '081660',
 '005870',
 '115160',
 '079980',
 '005010',
 '084110',
 '069260',
 '000540',
 '003280']

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
##https://antilibrary.org/2483 
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


