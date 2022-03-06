#The below code was used to scrpe the data for the application
#Note the link used in the web scraping i sfor educational purpose only

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import os
import pickle
import shutil

path=os.path.dirname(os.path.abspath("scrape.py"))

datalink='https://studyabroad.shiksha.com/usa/ms-colleges-dc'
# datalink="#"

agent = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}


with open(path+f'/data.csv','w') as file:

    file.write('Image,Universities,link,Public_university,Scholarship,Accommodation,Fees,TOEFL,IELTS,PTE,GRE\n')
    for i in range(25):
        if i==0:
            link=datalink
        else:
            # time.sleep(10)
            link=datalink+str(i+1)
        url=requests.get(link,headers=agent).text
        
        try:
            soup=BeautifulSoup(url,'lxml')
            ul=soup.find('ul',class_='tuple-cont')
            lis=ul.find_all('li')

        
            for li in lis:
                # time.sleep(1)
                if li.img:
                    try:
                        file.write(f"{li.img['src']},")
                    except :
                        file.write(f"{li.img['data-original']},")
                if(li.find('div',class_='tuple-detail')!=None):
                    file.write(li.find('div',class_='tuple-detail').div.a.text.replace(',',''))
                    file.write(f",{li.find('div',class_='tuple-detail').div.a['href']}")
                    box=li.find('div',class_='uni-course-details flLt')
                    dummy=box.find_all('p')
                    fs=dummy[len(dummy)-3:len(dummy)]
                    for f in fs:
                        if f.text.strip()[0]=='✔':
                            file.write(',1')
                        else:
                            file.write(',0')
                    cds=box.find_all('div')
                    for i,cd in enumerate(cds):
                        if(i==0):
                            if(cd.p==None):
                                file.write(',0')
                            else:
                                file.write(',{}'.format(cd.p.text.split(' ')[1]))
                        if(i==1):
                            exams=[0,0,0,0]
                            paras=cd.find_all('p')
                            for para in paras:
                                if(len(para.text.strip())<11):
                                    es=para.text.strip()
                                    x=es[:1]
                                    if(x=='T'):
                                        exams[0]=es.split(":")[1]
                                    if(x=='I'):
                                        exams[1]=es.split(":")[1]
                                    if(x=='P'):
                                        exams[2]=es.split(":")[1]
                                    if(x=='G'):
                                        exams[3]=es.split(":")[1]
                            for exam in exams:
                                file.write(f',{exam}')
                            file.write('\n')
        except: continue


shutil.copyfile(path+'/data.csv',path+'/data1.csv')
data=pd.read_csv(path+f'/data1.csv')
col=['Image','link']
pdata=data.drop(col,1)
pivot_data=pdata.set_index('Universities')
matrix_data=csr_matrix(pivot_data.values)
model=NearestNeighbors(metric='cosine',algorithm='brute')
model.fit(matrix_data)
pickle.dump(model,open(path+f'/college.pkl','wb'))
shutil.copyfile(path+'/college.pkl',path+'/college1.pkl')
