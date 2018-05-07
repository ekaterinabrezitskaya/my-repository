Ingredients = ('potato','carrot','onion','pepper','spaghetti','rice','tomato sauce','cucumber','green peas','chees')

Dishes={'1':'Soup','2':'Main dish','3':'Salad'}

Menu={
'Soup_chicken':'Chicken broth with egg',
'Soup_pork':'Hungarian goulash soup',
'Soup_beef':'Soup kharcho',
'Main dish_chicken':'Uzbek Pilaf',
'Main dish_pork':'Meat by French with potatoes',
'Main dish_beef':'Italian lasagna',
'Salad_chicken':'Caesar salad',
'Salad_pork':'Salad "Male caprice"',
'Salad_beef':'Salad Olivier'
}

Dish = input("\nWhat do you want on the dinner?\n \n 1.Soup \n 2.Main dish \n 3.Salad \n \nPlease, choose one number of dish from variants:")

if Dish in Dishes: 
   Meat = input("\n" + Dishes[Dish] +" "+ "must be with chicken, pork or beef?:")
   
   print("\n"'Great idea! {} with {} is {}'.format(Dishes[Dish],Meat,Menu[Dishes[Dish]+'_'+Meat]))
   
           if Menu[Dishes[Dish]+'_'+Meat] == 'Chicken broth with egg'
           print('You need to use for cooking:')
else:
   print ('You will be hungry')
  

conn = pymysql.connect(host='career.vubor.com', user='career_user',password='SoftBistro.2018', database='career')
cursor = conn.cursor()
cursor.execute("select id, vacancy_status from vacancy where vacancy_url=%s",(url_to_scrape))
result = cursor.fetchall()
gg=result[0][0]
status=result[0][1]

cursor.execute("INSERT INTO career.vacancy_description (vacancy_id,description, status) VALUES ('%s','fghdf','%s')", (gg,status))

conn.commit()



??