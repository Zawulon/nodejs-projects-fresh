import csv

with open('LinksToCrawl.csv', encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    accounts = []
    links = []
    for row in readCSV:
        account = row[4]
        link = row[1]

        accounts.append(account)
        links.append(link)

   #print(accounts)
   # print(link)

    # now, remember our lists?

    # whatColor = input('What color do you wish to know the date of?:')
    coldex = 3
    the1link = links[coldex]
    the1accc = accounts[coldex]
    print('The link of -',the1link,'- is: -',the1accc,'-')