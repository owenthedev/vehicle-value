# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:11:42 2022

@author: owen nxumalo, carl nxumalo
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup


#create function to get price
def get_price(url):
    #Set Up Scrape

    hheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    urlInput = url
    urlLen = len(urlInput)
    urlcut = urlInput[:urlLen-1]
    url=urlInput

    request=requests.get(url,headers=hheaders)
    content=request.content
    soup=BeautifulSoup(content,'lxml')

    #we now test if the the page has two pagination 
    text=[]
    empty=[]
    for pr in soup.find_all(class_="Pagination_pagination__71nnK"):
          text.append(pr.text)
    #getting the number of pages to scrape
    try: 
      leng= len(text[0])
      pages=0
      if leng<=21:
        text[0]=text[0].replace('Previous','')
        text[0]=text[0].replace('Next','')
        newlen = len(text[0])
        pages=int(text[0][newlen-1])
        print(pages)
      if leng>21:
        text[0]=text[0].replace('Previous12345678...','')
        text[0]=text[0].replace('Next','')
        pages=int(text[0])
        print(pages)

    except:
      pages=1
      print(pages)

    #putting the price and mileage in a list
    pricesa=[]
    raw=[]
    page = 1
    numpage=pages
    while page<=numpage:
      urlx=urlcut+str(page)
      request=requests.get(urlx,headers=hheaders)
      content=request.content
      soup=BeautifulSoup(content,'lxml')
      page = page+1
      for pr in soup.find_all(class_="price text-primary mb-2 Car_price__4Cc8z"):
          pricesa.append(pr.text)
      for ps in soup.find_all(class_="text-primary-gray"):
          raw.append(ps.text)
    print(pricesa)
    print(raw)
    print(raw[0])


    #removing the parts of the mileage list as there is unessary data included
    #length of mileage list
    rawL = len(raw)
    mileage=[]
    counting= 0
    for y in range(rawL-1):
      if counting < rawL:
        if "km" in raw[counting].lower():
          mileage.append(raw[counting])

        counting=counting+1
      else:
        y==rawL-1
    print(mileage)
    print(len(mileage))
    print(len(pricesa))
    
    # Change string to float and remove currency symbols
    sum=0
    sum2=0
    count=0
    pricesaNum=[]
    mileageNum=[]
    while count<(len(pricesa)):
      ord=pricesa[count][1:].replace(' ','')
      ord2=mileage[count]
      ord2=ord2.replace(' ','')
      ord2=ord2.replace('Km','')
      pricesaNum.append(float(ord))
      mileageNum.append(float(ord2))

      add=(float(ord))
      sum=sum+add

      count=count+1
    print('The sum:'+str(sum))
    print('the prices:'+str(pricesaNum))
    print('the mileage:'+str(mileageNum))
    
    # Sort list for summary statistics
    #pricesaNum.sort()
    #print(pricesaNum)
    
    #Summary Stats
    #Mean 
    arrlen=len(pricesaNum)
    
    mean=round(sum/arrlen,2)
    print("the mean is : "+str(mean))
    
    #median 
    #positionm=(arrlen+1)//2
    #median=pricesaNum[positionm]
    #print("the median is : "+str(median))
    
    #range 
    #smallest=pricesaNum[0]
    #largest=pricesaNum[arrlen-1]
    #ange=largest-smallest
    #print("the range is : "+str(ange))
    
    #min
    #min = pricesaNum[0]
    #print("the minimum is : "+str(min))
    
    #minimum 
    #max = pricesaNum[arrlen-1]
    #print("the maximum is : "+str(max))
    
    st.write('')
    st.write('')
    st.header('Your Car Valuation')
    st.write('the average price is: R',mean)
    

#UI
col1, col2 = st.columns(2)

with col1:
    st.image('https://raw.githubusercontent.com/owenthedev/vehicle-value/main/vehicle-value-logo.png',width=200)
    

with col2:
    st.title('VEHICLE VALUE CHECKER')
    st.audio('https://raw.githubusercontent.com/owenthedev/vehicle-value/main/SVT145%20-%20Aparde%20-%20Erosion%20(Free%20Track)%20-%20Master_V1_MP3.mp3')



st.write('Get a valuation for your car')

url_in = st.text_input(label='URL',value='')
if url_in=='':
    st.write('')
    st.write('')
    st.header('Please enter a URL above')
else:
    get_price(url_in)
    



