# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:11:42 2022

@author: owen nxumalo, carl nxumalo
"""

import streamlit as st
import requests
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from io import BytesIO
import xlsxwriter

hide_st_style="""
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)

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
    sum1=0
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
      sum1=sum1+add
      
      addm=(float(ord2))
      sum2=sum2+addm

      count=count+1
    print('The sum:'+str(sum1))
    print('the prices:'+str(pricesaNum))
    print('the mileage:'+str(mileageNum))
    
    # Sort list for summary statistics
    #pricesaNum.sort()
    #print(pricesaNum)
    
    #Summary Stats
    #Mean 
    arrlen=len(pricesaNum)
    
    mean=round(sum1/arrlen,2)
    print("the mean is : "+str(mean))
    meanm=round(sum2/arrlen,2)
    
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
    mins = min(pricesaNum)
    minm=min(mileageNum)
    #print("the minimum is : "+str(min))
    
    #minimum 
    maxs = max(pricesaNum)
    maxm=max(mileageNum)
    #print("the maximum is : "+str(max))
    
    ##### function to show the plot
    # x-axis values
    x = mileageNum
    # y-axis values
    y = pricesaNum
    
    ###### Create a dataframe
    cardf=pd.DataFrame()
    cardf['Price']=pricesaNum
    cardf['Mileage']=mileageNum
    ecardf=cardf
    
    # plotting points as a scatter plot
    plt.scatter(x, y, label= "Data Points", color= "green",
                marker= "x", s=15)
    slope,intercept,r,p,std_err=stats.linregress(cardf['Mileage'],cardf['Price'])
    def myfunc(x):
        return slope*x+intercept
    mymodel=list(map(myfunc, x))
    plt.plot(x,mymodel,color='black')
    # x-axis label
    plt.xlabel('Vehicle Mileage (km)')
    # frequency label
    plt.ylabel('Price (Rands)')
    # plot title
    plt.title('Plot of Vehicle Mileage and Price')
    # showing legend
    plt.legend()
    plt.savefig('chart.jpeg')
    

    ##### Create a csv file
    carcsv=cardf.to_csv(index=False)
    
    ##### Ceate an excel file
    #datatoexcel=pd.ExcelWriter("cardata.xlsx",engine='xlsxwriter')
    #carsexcel=ecardf.to_excel(datatoexcel, sheet_name="prices_mileage")
    output = BytesIO()

    # Write files to in-memory strings using BytesIO
    # See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','Mileage')
    worksheet.write('B1','Price')
    worksheet.write('C1','Search results URL')
    worksheet.write('C2',url)
    worksheet.write('D1','Average')
    worksheet.write('E1', '=AVERAGE(B2:B'+str(arrlen+1)+')')
    worksheet.write('D2','Minimum')
    worksheet.write('E2', '=MIN(B2:B'+str(arrlen+1)+')')
    worksheet.write('D3','Maximum')
    worksheet.write('E3', '=MAX(B2:B'+str(arrlen+1)+')')
    
    for a in range(0,arrlen):
        worksheet.write('B'+str(a+2),ecardf['Price'][a])
        worksheet.write('A'+str(a+2),ecardf['Mileage'][a])
    workbook.close()

    
    
   ####### Lin Reg Model
    def predictprice(cardf,mileage):
        slope,intercept,r,p,std_err=stats.linregress(cardf['Mileage'],cardf['Price'])
        price=slope*mileage+intercept
        return price
    ########### GUI ###############
                
    st.write('')
    st.header('Vehicle Market Data')
    st.write('Market cap: R',round(mean*arrlen/100000,2),'million')
    st.write('Number of similar listings: ',arrlen)
    markup = int(st.number_input('Insert dealer markup %',value=20))
    markup=markup/100.0
    colmile,coltrade, colmark = st.columns(3)
    
    with colmile:
        st.subheader('Market mileage (km)')
        st.write('average mileage is ',int(meanm))
        st.write('minimum mileage is ',int(minm))
        st.write('maximum mileage is ',int(maxm))
    
    with colmark:
        st.subheader('Market prices (rand)')
        st.write('average price is ',int(mean))
        st.write('minimum price is ',int(mins))
        st.write('maximum price is ',int(maxs))

    with coltrade:
        st.subheader('Trade-in prices (rand)')
        st.write('average price is ',int(round(mean*(1-markup),2)))
        st.write('minimum price is ',int(round(mins*(1-markup),2)))
        st.write('maximum price is ',int(round(maxs*(1-markup),2)))
    
    st.write('')

    st.header('Graph of Price vs Mileage')
    st.image('chart.jpeg', caption='Price vs Mileage',width=650)
    
    st.header('Price Prediction')
    age = st.slider('What is the mileage of the vehicle?', 0, int(1.5*max(cardf['Mileage'])), 30000)
    st.write("The predicted price is R:", int(predictprice(cardf, age)))
    
    st.write('')
    
    st.header('Explore Data')
    st.write('Get a better sense of the market value by comparing various prices and mileages')
    st.write("Click on 'Price' or 'Mileage' in the table to sort by them respectively")
    st.dataframe(cardf,width=1000)
    st.write('')
    st.subheader('Download Data')
    st.write('We believe in being open, so download the data below and calculate for yourself')
    st.download_button(
        label="Download Excel workbook",
        data=output.getvalue(),
        file_name="vehicle_value_car_data.xls",
        mime="application/vnd.ms-excel"
    )
    
    #st.download_button('Download Dataset EXCEL',carsexcel)
    st.download_button('Download Dataset CSV',carcsv,file_name='cardata.csv',key=2)
    
    

#UI
st.title('PriceSmiths Vehicle Valuer') 
st.write('Buy and Sell vehicles at the right price!')
st.write('Watch the video below for a demo')
url_in = st.text_input(label='Paste the URL here then press Enter',value='')
if url_in=='':
    st.write('')
    st.video('https://raw.githubusercontent.com/owenthedev/vehicle-value/main/how_to_value.mp4')
else:
    get_price(url_in)
    



