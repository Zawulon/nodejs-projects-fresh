import csv
import sqlite3


sqlite_file = 'pitax\pitax\spiders\sqlite.db'


insert_sql = "INSERT INTO [Ogranization_temp] ([Name],[Role],[SearchLink],[Phone],[Email],[Contact]) VALUES (?,?,?,?,?,?)"

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

with open('account_names.csv', encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    accounts = []
    for row in readCSV:
        account = row[0]
        link = row[3]
        role = row[4]
        phone = row[7]
        email = row[8]
        contact = row[9]
        
        list = []
        list.append(account)
        list.append(role)
        list.append(link)
        list.append(phone)
        list.append(email)
        list.append(contact)
        #list = [link, account]
       #colkeys = ['UrlToCrawl','Account']
      #  for ck in colkeys:
       #     list.append(item[ck])
        

       # for key in item.fields.keys():
       #     list.append(str(item[key])) 
        cur.execute(insert_sql, list)
        conn.commit()

   #print(accounts)
   # print(link)

    # now, remember our lists?

    # whatColor = input('What color do you wish to know the date of?:')
    #coldex = 3
    #the1link = links[coldex]
    #the1accc = accounts[coldex]
    #list = []
    #list.append(the1link)
    #list.append(the1accc)
    #cur.execute(insert_sql, list)
    #conn.commit()
    #print('The link of -',the1link,'- is: -',the1accc,'-')

    conn.close()