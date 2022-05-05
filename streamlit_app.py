# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:11:42 2022

@author: owen nxumalo, carl nxumalo
"""

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from io import BytesIO
import xlsxwriter


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
    mins = min(pricesaNum)
    #print("the minimum is : "+str(min))
    
    #minimum 
    maxs = max(pricesaNum)
    #print("the maximum is : "+str(max))
    
    ##### function to show the plot
    # x-axis values
    x = mileageNum
    # y-axis values
    y = pricesaNum

    # plotting points as a scatter plot
    plt.scatter(x, y, label= "Data Points", color= "green",
                marker= "+", s=15)

    # x-axis label
    plt.xlabel('Vehicle Mileage (km)')
    # frequency label
    plt.ylabel('Price (Rands)')
    # plot title
    plt.title('Plot of Vehicle Mileage and Price')
    # showing legend
    plt.legend()
    plt.savefig('chart.jpeg')
    

    def estimate_coef(x, y):
        # number of observations/points
        n = np.size(x)

        # mean of x and y vector
        m_x = np.mean(x)
        m_y = np.mean(y)

        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y*x) - n*m_y*m_x
        SS_xx = np.sum(x*x) - n*m_x*m_x

        # calculating regression coefficients
        b_1 = SS_xy / SS_xx
        b_0 = m_y - b_1*m_x

        return (b_0, b_1)

    def plot_regression_line(x, y, b):
        # plotting the actual points as scatter plot
        plt.scatter(x, y, color = "m",
                marker = ".", s = 14)

        # predicted response vector
        y_pred = b[0] + b[1]*x

        # plotting the regression line
        plt.plot(x, y_pred, color = "g")

        # putting labels
        plt.xlabel('x')
        plt.ylabel('y')

        # function to show plot
        plt.show()

    def main():
        # observations / data
        x = np.array(mileageNum)
        y = np.array(pricesaNum)

        # estimating coefficients
        b = estimate_coef(x, y)
        print("Estimated coefficients:\nb_0 = {} \
            \nb_1 = {}".format(b[0], b[1]))

      #enter your mileage 

        # plotting regression line
        plot_regression_line(x, y, b)

    if __name__ == "__main__":
        main()
    print(r)
    def myfunc(x):
      return slope * x + intercept

    
    
    
    ###### Create a dataframe
    cardf=pd.DataFrame()
    cardf['Price']=pricesaNum
    cardf['Mileage']=mileageNum
    ecardf=cardf
    ##### Create a csv file
    carcsv=cardf.to_csv(index=False)
    
    ##### Ceate an excel file
    datatoexcel=pd.ExcelWriter("cardata.xlsx",engine='xlsxwriter')
    carsexcel=ecardf.to_excel(datatoexcel, sheet_name="prices_mileage")
    output = BytesIO()

    # Write files to in-memory strings using BytesIO
    # See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','Price')
    worksheet.write('B1','Mileage')
    worksheet.write('C1','Search results URL')
    worksheet.write('C2',url)
    worksheet.write('D1','Average')
    worksheet.write('E1',str(mean))
    worksheet.write('D2','Minimum')
    worksheet.write('E2',str(mins))
    worksheet.write('D3','Maximum')
    worksheet.write('E3',str(maxs))
    for a in range(0,arrlen):
        worksheet.write('A'+str(a+2),ecardf['Price'][a])
        worksheet.write('B'+str(a+2),ecardf['Mileage'][a])
    workbook.close()

    
    
    ########### GUI ###############
    
 
    st.header('Vehicle Price Information')
    st.write('Note that dealerships need to make a profit when they buy a car from you. Therefore, the selling price of the car is higher than the price they bought the car for.')
    colnodeal, coldeal = st.columns(2)

    with coldeal:
        st.subheader('Prices others buy at')
        st.write('the average price is: R',mean)
        st.write('the minimum price is: R',mins)
        st.write('the maximum price is: R',maxs)

    with colnodeal:
        st.subheader('Prices you sell at')
        st.write('the average price is: R',round(mean*0.85,2))
        st.write('the minimum price is: R',round(mins*0.85,2))
        st.write('the maximum price is: R',round(maxs*0.85,2))
    
    st.write('')

    st.header('Graph of Price vs Mileage')
    st.image('chart.jpeg', caption='Price vs Mileage',width=400)
    
    number = st.number_input('Insert your mileage')
    predictedprice = myfunc(int(number))
    st.write('The price, given the mileage, is R',round(predictedprice,2))
    
    
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
        file_name="cardata.xlsx",
        mime="application/vnd.ms-excel"
    )
    
    #st.download_button('Download Dataset EXCEL',carsexcel)
    st.download_button('Download Dataset CSV',carcsv,file_name='cardata.csv',key=2)
    
    

#UI
col1, col2 = st.columns(2)

with col1:
    st.image('https://raw.githubusercontent.com/owenthedev/vehicle-value/main/vehicle-value-logoblk.png',width=200)
    

with col2:
    st.title('VEHICLE VALUE CHECKER')
    st.write('Get a good idea about the value of your car from us, an unbiased source.')
   



st.write('Step 1- Go to cars.co.za and search for your car there (select make, model year, mileage etc).')
st.write('Step 2- Copy the url and paste it into the text field.')
st.write('Need help? Watch the explainer video below')

url_in = st.text_input(label='Paste the URL here then press Enter',value='')
if url_in=='':
    st.write('')
    st.video('https://raw.githubusercontent.com/owenthedev/vehicle-value/main/how_to_value.mp4')
else:
    get_price(url_in)
    



