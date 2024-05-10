#!/usr/bin/env python3
import psycopg2
import datetime
from dateutil.relativedelta import relativedelta

#####################################################
##  Database Connection
#####################################################

"""
Connect to the database using the connection string
"""


def formatMenuItems(rows):
    i = 0
    result = []
    while i < len(rows):
        id = rows[i][0]
        name = rows[i][1]
        description = rows[i][2]
        category1 = rows[i][3]
        category2 = rows[i][4]
        category3 = rows[i][5]
        category = ""
        if category1 != None:
            category += category1
        if category2 != None:
            category += "|" + category2
        if category3 != None:
            category += "|" + category3

        coffeetype = rows[i][6]
        milkkind = rows[i][7]

        if coffeetype != None:
            option = coffeetype
            if milkkind != None:
                option += " - " + milkkind
        else:
            option = ""

        price = rows[i][8]
        if rows[i][9] != None:
            reviewdate = rows[i][9].strftime("%d-%m-%Y")
        else:
            reviewdate = ""

        if rows[i][10] != None:
            reviewer = rows[i][10] + " " + rows[i][11]
        else:
            reviewer = ""
        result.append(
            {
                "menuitem_id": id,
                "name": name,
                "description": description,
                "category": category,
                "coffeeoption": option,
                "price": price,
                "reviewdate": reviewdate,
                "reviewer": reviewer,
            }
        )

        i += 1
    return result


def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "y24s1c9120_alei5293"
    passwd = "Sunny445."
    myHost = "awsprddbs4836.shared.sydney.edu.au"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(
            database=userid, user=userid, password=passwd, host=myHost
        )
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)

    # return the connection to use
    return conn


"""
Validate staff based on username and password
"""


def checkStaffLogin(staffID, password):

    curs = openConnection().cursor()
    query = (
        f"SELECT * FROM staff WHERE staffID = '{staffID}' and password = '{password}'"
    )
    curs.execute(query)
    row = curs.fetchall()
    curs.close()
    if row == []:
        return None
    return list(row[0])


print(checkStaffLogin("jwalker", "876"))
"""
List all the associated menu items in the database by staff
"""


def findMenuItemsByStaff(staffID):
    # Establish a database connection and create a cursor
    curs = openConnection().cursor()

    # Query to select menu items reviewed by the given staff member
    query = f"""
SELECT m.menuitemid, m.name, m.description, cat1.categoryname as categoryname1, cat2.categoryname as categoryname2, cat3.categoryname as categoryname3, c.coffeetypename, mk.milkkindname, m.price, m.reviewdate, s.firstname, s.lastname 
FROM menuitem m LEFT OUTER JOIN category cat1 ON (m.categoryone = cat1.categoryid) 
				LEFT OUTER JOIN category cat2 ON (m.categorytwo = cat2.categoryid)
				LEFT OUTER JOIN category cat3 ON (m.categorythree = cat3.categoryid)
				LEFT OUTER JOIN coffeetype c ON (m.coffeetype = c.coffeetypeid)
				LEFT OUTER JOIN milkkind mk ON (m.milkkind = mk.milkkindid)
				LEFT OUTER JOIN staff s ON (m.reviewer = s.staffid)
WHERE m.reviewer = '{staffID}'
ORDER BY m.reviewdate, m.description DESC
            """


'''
Attempt # 2

CREATE VIEW viewingmenuitemlist AS
SELECT m.menuitemid, m.name, m.description, cat1.categoryname as categoryname1, cat2.categoryname as categoryname2, cat3.categoryname as categoryname3, c.coffeetypename, mk.milkkindname, m.price, m.reviewdate, s.firstname, s.lastname 
FROM menuitem m LEFT OUTER JOIN category cat1 ON (m.categoryone = cat1.categoryid) 
				LEFT OUTER JOIN category cat2 ON (m.categorytwo = cat2.categoryid)
				LEFT OUTER JOIN category cat3 ON (m.categorythree = cat3.categoryid)
				LEFT OUTER JOIN coffeetype c ON (m.coffeetype = c.coffeetypeid)
				LEFT OUTER JOIN milkkind mk ON (m.milkkind = mk.milkkindid)
				LEFT OUTER JOIN staff s ON (m.reviewer = s.staffid)
WHERE m.reviewer = 'johndoe'
ORDER BY m.reviewdate, m.description DESC;


SELECT menuitemid as ID, name, COALESCE(description, '') AS description,
CASE 
WHEN categoryname2 is NULL THEN categoryname1
WHEN categoryname3 is NULL THEN categoryname1 || '|' || categoryname2
WHEN categoryname3 is not NULL THEN categoryname1 || '|' || categoryname2 || '|' || categoryname3
END AS category, 
CASE 
WHEN (coffeetypename is NULL) and (milkkindname is NULL) THEN ''
WHEN (coffeetypename is not NULL) and (milkkindname is NULL) THEN coffeetypename
WHEN (coffeetypename is not NULL) and (milkkindname is not NULL) THEN coffeetypename || ' - ' || milkkindname
END AS option, 
price, 
TO_CHAR(reviewdate, 'DD-MM-YYYY') AS reviewdate, 
firstname || ' ' || lastname as reviewer
FROM viewingmenuitemlist

'''







    # Execute the query
    curs.execute(query)

    # Fetch all the rows
    rows = curs.fetchall()
    if rows == []:
        return None

    # Close the cursor
    curs.close()
    # print(rows)
    result = formatMenuItems(rows)

    # Return the list of menu items reviewed by the staff member
    # print(result)
    return result


"""
SQL Query for part 2. 

TO DO:
    - Change WHERE to the staffid 
    - Concatenate category names to "Breakfast" or "Breakfast|Lunch|Dinner" etc.
    - Concatenate c.coffeetypename and mk.milkkindname to Option
    - Concantenate s.firstname, s.lastname to name

SELECT m.menuitemid, m.name, m.description, cat1.categoryname as categoryname1, cat2.categoryname as categoryname2, cat3.categoryname as categoryname3, c.coffeetypename, mk.milkkindname, m.price, m.reviewdate, s.firstname, s.lastname 
FROM menuitem m LEFT OUTER JOIN category cat1 ON (m.categoryone = cat1.categoryid) 
				LEFT OUTER JOIN category cat2 ON (m.categorytwo = cat2.categoryid)
				LEFT OUTER JOIN category cat3 ON (m.categorythree = cat3.categoryid)
				LEFT OUTER JOIN coffeetype c ON (m.coffeetype = c.coffeetypeid)
				LEFT OUTER JOIN milkkind mk ON (m.milkkind = mk.milkkindid)
				LEFT OUTER JOIN staff s ON (m.reviewer = s.staffid)
WHERE m.reviewer = 'johndoe'
ORDER BY m.reviewdate, m.description DESC

"""


"""
Find a list of menu items based on the searchString provided as parameter
See assignment description for search specification
"""


def findMenuItemsByCriteria(searchString):
    # Establish a database connection and create a cursor
    curs = openConnection().cursor()
    today_date = datetime.datetime.now()
    oldest_date = today_date - relativedelta(years=10)
    print("oldest date",oldest_date)

    # Query to select menu items based on name or description containing the search string
    query = f"""
SELECT m.menuitemid, m.name, m.description, cat1.categoryname as categoryname1, cat2.categoryname as categoryname2, cat3.categoryname as categoryname3, c.coffeetypename, mk.milkkindname, m.price, m.reviewdate, s.firstname, s.lastname 
FROM menuitem m LEFT OUTER JOIN category cat1 ON (m.categoryone = cat1.categoryid) 
				LEFT OUTER JOIN category cat2 ON (m.categorytwo = cat2.categoryid)
				LEFT OUTER JOIN category cat3 ON (m.categorythree = cat3.categoryid)
				LEFT OUTER JOIN coffeetype c ON (m.coffeetype = c.coffeetypeid)
				LEFT OUTER JOIN milkkind mk ON (m.milkkind = mk.milkkindid)
				LEFT OUTER JOIN staff s ON (m.reviewer = s.staffid)
                WHERE (m.name ILIKE '%{searchString}%' OR m.description ILIKE '%{searchString}%' OR cat1.categoryname ILIKE '%{searchString}%' OR cat2.categoryname ILIKE '%{searchString}%' OR cat3.categoryname ILIKE '%{searchString}%' OR c.coffeetypename ILIKE '%{searchString}%' OR mk.milkkindname ILIKE '%{searchString}%' or s.firstname ILIKE '%{searchString}%' or s.lastname ILIKE '%{searchString}%') And (m.reviewdate >= '{oldest_date}' or m.reviewdate is null)
                ORDER BY s.firstname desc, m.reviewdate desc
            
            """


TO_CHAR(CURRENT_TIMESTAMP, 'dd-mm-yyyy')

    # Execute the query
    curs.execute(query)

    # Fetch all the rows
    rows = curs.fetchall()

    if rows == []:
        return None
    # Close the cursor
    print(rows)
    result = formatMenuItems(rows)
    curs.close()

    # Return the list of menu items matching the search criteria
    return result

'''
SELECT m.menuitemid, m.name, m.description, cat1.categoryname as categoryname1, cat2.categoryname as categoryname2, cat3.categoryname as categoryname3, c.coffeetypename, mk.milkkindname, m.price, m.reviewdate, s.firstname, s.lastname 
FROM menuitem m LEFT OUTER JOIN category cat1 ON (m.categoryone = cat1.categoryid) 
				LEFT OUTER JOIN category cat2 ON (m.categorytwo = cat2.categoryid)
				LEFT OUTER JOIN category cat3 ON (m.categorythree = cat3.categoryid)
				LEFT OUTER JOIN coffeetype c ON (m.coffeetype = c.coffeetypeid)
				LEFT OUTER JOIN milkkind mk ON (m.milkkind = mk.milkkindid)
				LEFT OUTER JOIN staff s ON (m.reviewer = s.staffid)
WHERE 	(LOWER(m.name) like '%fee%' OR 
		LOWER(m.description) like '%fee%' OR 
		LOWER(cat1.categoryname) like '%fee%' OR 
		LOWER(cat2.categoryname) like '%fee%' OR 
		LOWER(cat3.categoryname) like '%fee%' OR 
		LOWER(c.coffeetypename) like '%fee%' OR 
		LOWER(mk.milkkindname) like '%fee%' OR 
		LOWER(s.firstname) like '%fee%' OR 
		LOWER(s.lastname) like '%fee%') AND 
		(m.reviewdate > '2014/05/03' OR m.reviewdate IS NULL)
ORDER BY s.firstname DESC, m.reviewdate DESC


'''






"""
Add a new menu item
"""

def getCategoryId(category):
    curs = openConnection().cursor()
    query = f"SELECT categoryid FROM category WHERE categoryname = '{category}'"
    curs.execute(query)
    row = curs.fetchall()
    curs.close()
    if row == []:
        return None
    return row[0][0]

def getCoffeeTypeId(coffeetype):
    curs = openConnection().cursor()
    query = f"SELECT coffeetypeid FROM coffeetype WHERE coffeetypename = '{coffeetype}'"
    curs.execute(query)
    row = curs.fetchall()
    curs.close()
    if row == []:
        return None
    return row[0][0]

def getMilkKindId(milkkind):
    curs = openConnection().cursor()
    query = f"SELECT milkkindid FROM milkkind WHERE milkkindname = '{milkkind}'"
    curs.execute(query)
    row = curs.fetchall()
    curs.close()
    if row == []:
        return None
    return row[0][0]

def none_if_empty_otherwise_int_value(value):
    if value == '':
        return None
    return int(value)
def checkLength(value, length):
    if len(value) > length:
        return False
    return True
def addMenuItem(
    name,
    description,
    categoryone,
    categorytwo,
    categorythree,
    coffeetype,
    milkkind,
    price,
):
    # Establish a database connection and create a cursor
    conn = openConnection()
    curs = conn.cursor()
        
    categoryone = categoryone.strip().lower()
    categorytwo = categorytwo.strip().lower()
    categorythree = categorythree.strip().lower()
    coffeetype = coffeetype.strip().lower()
    milkkind = milkkind.strip().lower()
    description = description.strip()

    # Query to insert a new menu item into the MenuItem table
    if name == '' or categoryone == '' or price == '':
        return False
    
    if coffeetype == '' and milkkind != '':
        return False
    
    if getCategoryId(categoryone) == None:
        return False
    if categorytwo != '' and getCategoryId(categorytwo) == None:
        return False
    if categorythree != '' and getCategoryId(categorythree) == None:
        return False
    

    categoryone = getCategoryId(categoryone)

    categorytwo = getCategoryId(categorytwo)
    categorythree = getCategoryId(categorythree)
    coffeetype = getCoffeeTypeId(coffeetype)
    milkkind = getMilkKindId(milkkind)

    if categorytwo == None and categorytwo != '':
        return False
    if categorythree == None and categorythree != '':
        return False
    if coffeetype == None and coffeetype != '':
        return False
    if milkkind == None and milkkind != '':
        return False
    
    if not checkLength(name, 30):
        return False
    if not checkLength(description, 150):
        return False
    
    if description == '':
        description = None
    categorytwo = none_if_empty_otherwise_int_value(categorytwo)
    categorythree = none_if_empty_otherwise_int_value(categorythree)
    coffeetype = none_if_empty_otherwise_int_value(coffeetype)
    milkkind = none_if_empty_otherwise_int_value(milkkind)
    try:
        price = round(float(price),2)
    except:
        return False
    

    query = f"""
            INSERT INTO MenuItem (Name, Description, CategoryOne, CategoryTwo, CategoryThree, CoffeeType, MilkKind, Price)
            VALUES ('{name}','{description}',{categoryone}, {categorytwo}, {categorythree}, {coffeetype}, {milkkind}, {price})
            """

    try:
        # Execute the query
        curs.execute(query)
        # Commit the transaction
        conn.commit()
        # Close the cursor and connection
        curs.close()
        conn.close()
        return True  # Return True if the item was added successfully
    except Exception as e:
        # If an error occurs, rollback the transaction and return False
        conn.rollback()
        curs.close()
        conn.close()
        print("Error:", e)
        return False


"""
Update an existing menu item
"""


def updateMenuItem(
    name,
    description,
    categoryone,
    categorytwo,
    categorythree,
    coffeetype,
    milkkind,
    price,
    reviewdate,
    reviewer,
):
    # Establish a database connection and create a cursor
    conn = openConnection()
    curs = conn.cursor()

    # Query to update an existing menu item in the MenuItem table
    query = f"""
            UPDATE MenuItem 
            SET Description = '{description}', 
                CategoryOne = {categoryone}, 
                CategoryTwo = {categorytwo}, 
                CategoryThree = {categorythree}, 
                CoffeeType = {coffeetype}, 
                MilkKind = {milkkind}, 
                Price = {price}, 
                ReviewDate = '{reviewdate}', 
                Reviewer = '{reviewer}'
            WHERE Name = '{name}'
            """

    try:
        # Execute the query
        curs.execute(query)
        # Commit the transaction
        conn.commit()
        # Close the cursor and connection
        curs.close()
        conn.close()
        return True  # Return True if the item was updated successfully
    except Exception as e:
        # If an error occurs, rollback the transaction and return False
        conn.rollback()
        curs.close()
        conn.close()
        print("Error:", e)
        return False
