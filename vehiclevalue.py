# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:11:42 2022

@author: owenn
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup


col1, col2 = st.columns(2)

with col1:
    st.image('https://raw.githubusercontent.com/owenthedev/vehicle-value/main/vehicle-value-logo.png',width=200)

with col2:
    st.title('VEHICLE VALUE CHECKER')
    st.audio('https://raw.githubusercontent.com/owenthedev/vehicle-value/main/SVT145%20-%20Aparde%20-%20Erosion%20(Free%20Track)%20-%20Master_V1_MP3.mp3')



st.write('Get a valuation for your car')


url = st.text_input(label='URL',value='https://www.cars.co.za/usedcars.php?make_model_variant=Hyundai[i20][1.2]&sort=date_d&vfs_year=2022-2022|2021-2021|2020-2020|2019-2019|2018-2018&P=')


#Set Up Scrape
hheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
#urlInput = str(input("paste url from cars.co.za : "))
#urlLen = len(urlInput)
#urlcut = urlInput.replace('1','')
request=requests.get(url,headers=hheaders)
content=request.content
soup=BeautifulSoup(content,'lxml')
text=[]
for pr in soup.find_all(class_="Pagination_pagination__71nnK"):
      text.append(pr.text)
#getting the number of pages to scrape
leng= len(text[0])
pages=0
if leng<=20:
  text[0]=text[0].replace('Previous','')
  text[0]=text[0].replace('Next','')
  newlen = len(text[0])
  pages=int(text[0][newlen-1])
  print(pages)
if leng>=20:
  text[0]=text[0].replace('Previous12345678...','')
  text[0]=text[0].replace('Next','')
  pages=int(text[0])
  print(pages)
  
# Scrape site
pricesa=[]
page = 0
numpage=pages
urlfixed=url
while page<numpage:
  url=urlfixed+str(page)
  
  request=requests.get(url,headers=hheaders)
  content=request.content
  soup=BeautifulSoup(content,'lxml')
  page = page+1
  for pr in soup.find_all(class_="price text-primary mb-2 Car_price__4Cc8z"):
      pricesa.append(pr.text)
  
print(pricesa)

# Change string to float and remove currency symbols
sum=0
count=0
pricesaNum=[]
while count<(len(pricesa)):
  ord=pricesa[count][1:].replace(' ','')
  pricesaNum.append(float(ord))
  add=(float(ord))
  sum=sum+add
  count=count+1
print(sum)
print(pricesaNum)

# Sort list for summary statistics
pricesaNum.sort()
print(pricesaNum)

#Summary Stats
#Mean 
arrlen=len(pricesaNum)

mean=round(sum/arrlen,2)
print("the mean is : "+str(mean))

#median 
positionm=(arrlen+1)//2
median=pricesaNum[positionm]
print("the median is : "+str(median))

#range 
smallest=pricesaNum[0]
largest=pricesaNum[arrlen-1]
ange=largest-smallest
print("the range is : "+str(ange))

#min
min = pricesaNum[0]
print("the minimum is : "+str(min))

#minimum 
max = pricesaNum[arrlen-1]
print("the maximum is : "+str(max))

st.write('')
st.write('')
st.header('Your Car Valuation')
st.write('the average price is: R',mean)
st.write('the median price is: R',median)
st.write('the range of the prices is: R',ange)


