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

# # 네이버금융 재무제표 크롤러 
#
# ## 최종 버전 
# #### 이전 버전은 같은 폴더 내 다른 소스코드 참고. 
#
# ### (2021.04.15) 1019개 기업 재무제표 크롤링 완료. 
# ### 16년부터 20년까지의 연간 재무제표
# #### try, except 문을 써서 상장폐지된 기업은 예외처리함. 
#

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

before_list = '''
000030 000040 000050 000060 000070 000080 000100 000110 000120 000140 000150 000180 000210 000220 000230 000240 000250 000270 000300 000320 000370 000390 000400 000430 000480 000490 000500 000520 000540 000590 000640 000650 
000660 000670 000680 000700 000720 000760 000810 000850 000860 000880 000890 000910 000950 000970 000990 001020 001040 001060 001070 001080 001120 001130 001140 001200 001210 001230 001250 001260 001270 001290 001340 001360
001380 001390 001420 001430 001440 001450 001460 001470 001500 001510 001520 001530 001550 001560 001570 001620 001630 001680 001720 001740 001750 001770 001780 001790 001800 001820 001880 001940 002000 002020 002030 002070
002100 002140 002150 002170 002200 002210 002220 002240 002250 002270 002300 002310 002320 002350 002360 002380 002390 002410 002420 002450 002460 002550 002600 002620 002630 002690 002700 002710 002720 002760 002780 002790
002810 002820 002840 002870 002880 002900 002920 002960 002990 003000 003010 003030 003060 003070 003080 003090 003120 003160 003200 003220 003230 003240 003280 003300 003350 003380 003410 003450 003460 003470 003480 003490
003520 003530 003540 003550 003560 003570 003580 003610 003620 003650 003670 003680 003690 003720 003780 003830 003850 003920 003960 004000 004020 004060 004080 004090 004100 004130 004140 004150 004170 004200 004250 004270
004310 004360 004370 004380 004410 004430 004440 004450 004490 004540 004560 004690 004700 004710 004720 004740 004770 004800 004830 004840 004870 004890 004910 004920 004940 004960 004970 004980 004990 005010 005030 005070
005090 005110 005180 005190 005250 005270 005280 005290 005300 005320 005360 005380 005390 005420 005430 005440 005450 005490 005500 005610 005620 005680 005690 005720 005740 005750 005800 005810 005820 005830 005850 005870
005880 005930 005940 005950 005960 005980 005990 006040 006060 006090 006110 006120 006200 006220 006260 006280 006340 006350 006360 006370 006380 006390 006400 006490 006570 006650 006660 006730 006740 006800 006840 006880 
006890 006980 007070 007110 007120 007160 007190 007210 007280 007310 007330 007340 007390 007460 007540 007570 007590 007610 007630 007660 007690 007700 007810 007820 007860 007980 008000 008040 008060 008110 008250 008260 
008270 008350 008420 008490 008500 008560 008600 008670 008700 008730 008770 008870 008930 008970 009070 009140 009150 009160 009180 009190 009200 009240 009270 009290 009310 009320 009410 009420 009440 009450 009460 009470 009520 009540 009580 009680 009770 009810 009830 009970 010040 010050 010060 010100 010120 010130 010140 010170 010400 010420 
010470 010580 010600 010620 010640 010660 010690 010770 010780 010820 010950 010960 011000 011040 011070 011090 011150 011160 011170 011200 011210 011230 011280 011300 011330 011390 011420 011500 011690 011700 011720 011760
011780 011790 011810 011930 012030 012160 012170 012200 012280 012320 012330 012450 012510 012600 012610 012630 012690 012700 012750 012800 013000 013030 013120 013360 013520 013570 013580 013700 013870 014130 014160 014280 014440 014470 014530 014580 014620 014680 014710 014790
014820 014830 014910 014990 015020 015230 015260 015350 015360 015540 015590 015750 015760 015860 015890 016090 016100 016170 016250 016360 016380 016450 016580 016590 016600 016610 016710 016740 016800 016830 016880 017040
017180 017370 017390 017550 017670 017800 017810 017900 017940 017960 018250 018260 018310 018470 018500 018670 018880 019170 019180 019210 019300 019440 019490 019550 019570 019590 019680 020000 020120 020150 020560 020760
021050 021080 021240 021320 021820 021880 021960 022100 023000 023150 023350 023410 023450 023460 023530 023590 023760 023800 023810 023890 023960 024070 024090 024110
024660 024720 024890 024900 025000 025530 025540 025560 025620 025750 025770 025820 025860 025890 025900 025980 026180 026890 026940 026960 027050 027360 027390 027410 027740 027830 027970 028050 028080 028100 028150
028260 028300 028670 029460 029530 029780 029960 030000 030190 030200 030210 030520 030530 030610 030720 030790 031390 031430 031440 031820 031980 032190 032350 032500 032560 032620
032640 032710 032830 032850 033160 033170 033180 033240 033250 033270 033290 033530 033660 033780 033920 034020 034120 034220 034230 034300 034310 034590 034730 034830 035000 035080 035150 035250 035420 035510 035600 035720
035760 035900 036030 036420 036460 036490 036530 036540 036560 036570 036580 036710 036800 036830 036890 036930 037270 037560 037620 037710 038060 038500 038540 039020 039030 039130 039200 039490 039570 039840 039860 041140
041190 041440 041510 041520 041650 041830 041960 042000 042370 042420 042660 042670 042700 043150 043370 043610 044340 044380 044450 044490 044820 045390 045890 046140 046440 046890 047040 047050 047400 047770
047810 048260 048530 049520 049770 049800 049950 049960 051370 051500 051600 051630 051900 051910 052020 052260 052400 052690 052770 052790 053030 053210 053300 053350 053690 053800 054050 054620 054670 054800 054950 055490
055550 056190 056700 057050 057500 058430 058470 058650 058730 058820 058850 058860 060000 060150 060250 060370 060560 060570 060720 060980
063080 063160 064240 064350 064760 064960 065060 065160 065620 065660 066270 066570 066970 067000 067080 067160 067170 067280 067290 067630 067830 067900 068240 068270 068290 068400 068760 068870 069080 069110 069260 
069460 069620 069640 069730 069960 070300 070590 070960 071050 071090 071320 071840 071950 071970 072130 072470 072710 072870 073070 073240 074610 075180 075580 077360 077500 077970 078000 078020 078070 078150 078160 078340
078520 078930 079160 079430 079440 079550 079660 079980 080160 080420 081000 081660 081970 082270 082640 082740 083420 083790 084010 084110 084370 084670 084680 084690 084870 084990 085310 085370 085620 085660 086280 086390
086450 086520 086790 086900 086980 087010 088130 088350 088390 088790 089030 089470 089590 089600 090080 090350 090360 090370 090430 090460 091090 091700 091810 091990 092040
092070 092200 092220 092230 092440 092730 092780 093050 093230 093240 093370 094280 094480 094840 095340 095570 095610 095660 095700 095720 096530 096760 096770 097230 097950 098460 099190 099660 100120
100220 100250 100840 101060 101140 101530 102260 102280 102460 102940 103130 103140 103590 104110 104120 104480 104700 104830 105560 105630 105840 107590 108230 108320 108670 108790 109070 111110 111770 112040 112610 114090
114120 114570 115160 115180 115390 115450 115960 117580 117930 118000 119610 119650 120030 120110 121440 122870 122900 123420 123690 123700 123890 126560 128820 128940 129260 130660 130960 131970 133820 134380 134790 136480
136490 138040 138250 138490 138930 139130 139480 140410 141080 143210 143240 144510 144620 145020 145210 145720 145990 149980 151860 151910 152330 155660 161000 161390 161890 163560 168330 170900 171120 175330 178780 178920
180640 181710 182400 183190 183490 185750 192080 192400 192440 192520 192530 192820 194370 194480 195870 197210 200130 200230 200670 200880 204320 204620 206640 207940 208340 210540
210980 213090 213420 213500 214320 214330 214370 214390 214420 214450 215000 215600 216050 217730 218410 221610 222040 226320 226950 227840 229640 234080 237690 237880 240810 241520 241560 241590 243070 246690
248170 249420 251270 253450 263750 264900 265520 267250 267260 267270 267290 267850 267980 268280 271560 271980 272290 272450 272550 280360 281820 282330 282690 284740 285130 286940 293480 293580 294870 298000 298020 298040 298050
298690 300720 306200 316140 800172 800197 801190 801688 804337 804504 805087 805992 807958 809337 811097 811323 813002 813363 814270 815419 818158 818586 818905 828519 828992 829322 832969 836248 839185 839683 839719 839723
839742 854231 855981 856659 860086 861717 867865 879070 888975 
'''  

company_list = before_list.split()

company_list


def stock_crawler(code):
    
    browser.maximize_window()
    
    name = code
    base_url = 'https://finance.naver.com/item/coinfo.nhn?code='+ name + '&target=finsum_more'
    
    
    browser.get(base_url)
    time.sleep(1.5)
   
    browser.switch_to_frame(browser.find_element_by_id('coinfo_cp'))
    time.sleep(1.5)
    
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[3]')[0].click()
    time.sleep(1.5)

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
    
    browser.close()
    
    
    ###일단 어떤게 필요할지 몰라 다 들고왔지만 5개년, 즉 5행까지만 쓰는 걸로 잠정적 결론.
    df.drop(df.index[5:], inplace=True)
    time.sleep(1)
    
    
    return df

browser  = Chrome()

df_first_row = stock_crawler('000020')

df_first_row

for i in company_list :
    
    browser  = Chrome()
    
    try : 
        df_new = stock_crawler(i)
        df_first_row = pd.concat([df_first_row, df_new])
        
    except:
        browser.close()
        time.sleep(1)
        continue

#엑셀로 변환
df_all = df_first_row
df_all.to_excel('tobinq.xlsx')


