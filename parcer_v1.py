import re
import requests
from bs4 import BeautifulSoup
import pymysql
import pymysql.cursors
import html
import string
from collections import Counter

#connect to database
conn = pymysql.connect(host='career.vubor.com', user='career_user',password='SoftBistro.2018', database='career', charset='utf8')
cursor = conn.cursor()

#catch explorer.query
n='1' #career.explorer.status
cursor.execute("SELECT  career.explorer.id, career.explorer.query FROM career.explorer WHERE explorer.status = %s", (n))
resulty = cursor.fetchall()
cursor.execute("SELECT count(*) FROM career.explorer WHERE explorer.status = %s", (n))
iterations = cursor.fetchall()
if iterations[0][0] == 0:
       print ("No one query for update")
for j in range (0,iterations[0][0]):
    url_search = resulty[j][1] #url_search: https://www.work.ua/ua/jobs-data-scientist/
    e_id= resulty[j][0]        #explorer_id of career.vacancy
    s = requests.get(url_search)
    soup_s = BeautifulSoup(s.text)
    print('Now will be collected info about ' + resulty[j][1])
         
#urls of all_pages
    main_ul = soup_s.find('ul', class_="pagination hidden-xs")
    qty_pages = int(main_ul.find_all('a', href=True)[-2].text)
    all_pages = []  #list urls on all_pages
    for page in range(1,qty_pages+1):
       all_pages.append(resulty[0][1]+'?ss=1&page='+str(page))
    print('Info about this consist of ' + str(qty_pages) + ' pages')
    
#create the list of urls of vacancy from all pages
    urls = []  #list urls of vacancy from all pages
    for page in all_pages:
       each_page = requests.get(page)
       soup_each_page = BeautifulSoup(each_page.text) # full page of site
       for a in soup_each_page.find_all('a', href=True):
          if a['href'][:9]=='/ua/jobs/' and len(a['href'])==17:
              urls.append("https://www.work.ua"+a['href'])
    print('Total number of vacancies:' + str(len(urls)//2+1))

#check urls in database and insert distinct urls/description
    z = 0
    for link_url in urls:    
        v_st ='2'          #vacancy_status of career.vacancy
        ex_id = e_id       #explorer_id of career.vacancy
        cursor.execute("Select count(*) from career.vacancy where vacancy_url=%s", (link_url))
        result = cursor.fetchall()
        if result[0][0]==0:
            cursor.execute("INSERT INTO career.vacancy (explorer_id,vacancy_url,vacancy_status) VALUES (%s,%s,%s)", (ex_id,link_url,v_st))
            r = requests.get(link_url)
            soup = BeautifulSoup(r.text) # full page of vacancy
            main_div = soup.find('div', {'class': 'card wordwrap'})
            paragraphs=[]
            for tag in main_div.h2.next_siblings:
                paragraphs.append(tag)
            t=''
            for i in range(0,len(paragraphs)-4):
                if type(paragraphs[i]).__name__=='Tag':
                    t=t+str(paragraphs[i].get_text())+' '
                v_descr=''
                for tt in t:
                    if tt!="\uFFFD" and tt!="\u2014":
                        v_descr=v_descr+str(tt)
            cursor.execute("select id, vacancy_status from vacancy where vacancy_url=%s",(link_url))
            result = cursor.fetchall()
            v_id=result[0][0]
            cursor.execute("INSERT INTO career.vacancy_description (vacancy_id,description,status) VALUES ('%s',%s,%s)", (v_id,v_descr,n))
            z = z + 1
            if (z%20)==0:
                print ('More than '+str(z)+' vacancies are added into the database')
    cursor.execute("UPDATE career.explorer SET explorer.status = 2 WHERE explorer.query=%s",(str(url_search)))
    urls.clear()
    conn.commit()                   
    print('Finish! '+str(z)+' vacancies descriptions were processed')
conn.close()

#connect to database
conn = pymysql.connect(host='career.vubor.com', user='career_user',password='SoftBistro.2018', database='career', charset='utf8')
cursor = conn.cursor()
#define all_words for each vacancy

#the_string[i][0] #career.vacancy_description.id
#the_string[i][1] #career.vacancy_description.description

i=0
skill_id = 0
words_type = 0

cursor.execute("select career.vacancy_description.id, career.vacancy_description.description, career.vacancy.vacancy_url from career.vacancy_description join career.vacancy on career.vacancy.id = career.vacancy_description.vacancy_id where career.vacancy_description.status = %s", (n))
the_string = cursor.fetchall()

cursor.execute("select Count(*) from career.vacancy_description join career.vacancy on career.vacancy.id = career.vacancy_description.vacancy_id where career.vacancy_description.status = %s", (n))
the_count = cursor.fetchall()
count_desc=the_count[0][0]

r=0
for i in range(0,count_desc):
  n_id = the_string[i][0]
  cursor.execute("select count(*) from career.vacancy_words where vacancy_description_id = %s", (n_id))
  count = cursor.fetchall()   
  if count[0][0]==0:
    d=str(the_string[i][1])
    d=d.lower().replace('\xa0',' ').replace('\n',' ')
    for junk_char in "%$@*.!&,„“:;•/\—)[]‘+(»«":
      d = d.replace(junk_char, ' ')
    all_words=[word.strip(string.punctuation) for word in d.split()]
    word_quantity = Counter(all_words)
    word_dict = dict(word_quantity)
    for key in word_dict:
      if len(key)>2:
         cursor.execute("INSERT INTO career.vacancy_words (vacancy_description_id, word, qty, skill_id, type) VALUES (%s,%s,%s,%s,%s)", (the_string[i][0],key,word_dict[key],skill_id,words_type))
         cursor.execute("UPDATE career.vacancy_description SET vacancy_description.status = 2 WHERE vacancy_description.id=%s",(the_string[i][0]))
         conn.commit()
    r = r + 1
    if (r%10)==0:
        print ('More than '+str(r)+' vacancies description were divided on words')
        
print('Finish! '+str(r)+' vacancies descriptions were divided on words') 
conn.close()
         
      
