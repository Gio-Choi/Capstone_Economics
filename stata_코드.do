gen y1=real(per)
replace y2=real(y2)
gen y3=real(토빈의Q)
tab 환경  //
destring y2, replace 

gen x11=6 if 환경등급=="A+"
replace x11=5 if 환경등급=="A"
replace x11=4 if 환경등급=="B+"
replace x11=3 if 환경등급=="B"
replace x11=2 if 환경등급=="C"
replace x11=1 if 환경등급=="D"

gen x12=6 if 사회등급=="A+"
replace x12=5 if 사회등급=="A"
replace x12=4 if 사회등급=="B+"
replace x12=3 if 사회등급=="B"
replace x12=2 if 사회등급=="C"
replace x12=1 if 사회등급=="D"

gen x13=6 if 지배구조등급=="A+"
replace x13=5 if 지배구조등급=="A"
replace x13=4 if 지배구조등급=="B+"
replace x13=3 if 지배구조등급=="B"
replace x13=2 if 지배구조등급=="C"
replace x13=1 if 지배구조등급=="D"

gen x14=6 if 통합등급=="A+"
replace x14=5 if 통합등급=="A"
replace x14=4 if 통합등급=="B+"
replace x14=3 if 통합등급=="B"
replace x14=2 if 통합등급=="C"
replace x14=1 if 통합등급=="D"

destring 총자산, replace ignore(",")
gen lnAsset=ln(총자산)


su x14
tab x14
tab no x14




reg y1 x11 x12 x13 lnAsset
reg y1 x14 

* 횡단면 데이터 : Pooled OLS: firm이 반복적으로 포함되는 사실을 고려하지 않는다.
* 패널 regression : 반복적으로 나타남 둘 다 넣으라고


encode 기업코드, gen(firm)
xtreg  y1 x11 x12 x13 lnAsset lnRevenue, re i(firm)
xtreg  y1 x14 lnAsset lnRevenue, re i(firm)
xtreg  y3 x14 lnAsset roa der, re i(firm)
xtreg  y3 x11 x12 x13 lnAsset roa der, re i(firm)

xtreg  y1 x11 x12 x13 lnAsset roa der, fe i(firm)
xtreg  y1 x14 lnAsset roa, fe i(firm)
xtreg  y3 x14 lnAsset roa der, fe i(firm)
xtreg  y3 x11 x12 x13 lnAsset roa der, fe i(firm)
* re거나 fe거나 확률효과 or 고정효과



운수창고
estimate table Model // 이거를 copy table 한글이나 워드로 들고가서 표로 만들면 됨..!!!)

drop if 산업분류 == "금융" || 산업분류 =="철강금속" || 산업분류 =="유통업" ||산업분류 == "섬유의복" ||산업분류 =="음식료품"||산업분류 =="의약품"||산업분류 == "서비스업"||산업분류 == "에너지"||산업분류 =="기타제조업"||산업분류 =="운수창고"     
