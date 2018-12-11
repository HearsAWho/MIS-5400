import sqlite3
import urllib3
from statistics import mean
from bs4 import BeautifulSoup


# open DB and create table
conn = sqlite3.connect('REIT.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE AllReits (ticker text, name text , price real, divYield real, mktCap real, pe real, payout real)')
print ("Table created successfully")
conn.commit()
conn.close()

print("Scrapping data:")


http = urllib3.PoolManager()
r = http.request('GET','https://www.suredividend.com/reit-list/')
r.status
soup = BeautifulSoup(r.data)


#look at all tables to find the class for the one we need
all_tables = soup.find_all('table')

# now only look at the table we want
soup.find_all('table', id= 'table_1')
our_table = soup.find('table' , {'id' : 'table_1'})
# print(our_table.prettify())

# setup lists to store data temporarily until we put it into a database
aList = []
bList = []
cList = []
dList = []
eList = []
fList = []
gList = []


# add data to lists
for row in our_table.findAll('tr'):
    cells = row.findAll('td')
    states = row.findAll('th')
    if len(cells) == 7:
        aList.append(cells[0].find(text=True))
        bList.append(cells[1].find(text=True))
        cList.append(cells[2].find(text=True))
        dList.append(cells[3].find(text=True))
        eList.append(cells[4].find(text=True))
        fList.append(cells[5].find(text=True))
        gList.append(cells[6].find(text=True))
print("data scraped")


#now that we have the raw input, clean it
# pop last element as it is garbage data
aList = aList[:-1]
bList = bList[:-1]
cList = cList[:-1]
dList = dList[:-1]
eList = eList[:-1]
fList = fList[:-1]
gList = gList[:-1]

# convert market cap to str to remove comma's then store as double
for row in range(0,len(eList)):
    if cList[row]: cList[row] = float(str(cList[row]).replace(',',''))
    if dList[row]: dList[row] = float(str(dList[row]).replace(',',''))
    if eList[row]: eList[row] = float(str(eList[row]).replace(',',''))
    if fList[row]: fList[row] = float(str(fList[row]).replace(',',''))
    if gList[row]: gList[row] = float(str(gList[row]).replace(',',''))

#insert cleaned data to DB
print("adding data to DB")
with sqlite3.connect("REIT.db") as con:
    for i in range(0,int(len(aList))): 
        cur = con.cursor()
        cur.execute("INSERT INTO AllReits (ticker,name,price,divYield,mktCap,pe,payout) VALUES (?,?,?,?,?,?,?)",
                (aList[i], bList[i], cList[i], dList[i], eList[i], fList[i], gList[i]))
        con.commit()
con.close()
print ("Insert successful")




# filter down from allReits to those that we would consider invest-worthy based on existing data
#  eps(can calc from price and pe)

with sqlite3.connect("REIT.db") as con:
    cur = con.cursor()
    con.execute(
        'CREATE TABLE goodReits (ticker text, name text , price real, divYield real, mktCap real, pe real, payout real)')
    cur.execute("insert into goodReits "
                "SELECT * FROM AllReits WHERE divYield > 8 and pe < 14 and mktCap > 250;")
con.close()



# for version 2:
# take 'investment worthy' reits and pull dividend history, 1 year price target,forward pe,
# find trend of dividend and remove downtrending REITS?
# store new data in new div history table and link to allReits via ticker




#############################
#"""# personal help code:"""
# reconnect and pull the data to confirm integrity
conn = sqlite3.connect('REIT.db')
c = conn.cursor()

# select * from the table I already created previously
c.execute(
    '''
    select * from goodReits

    '''
    )
print (c.fetchall())
c.close()
conn.close()

