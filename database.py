#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "y24s1c9120_alei5293"
    passwd = "Sunny445."
    myHost = "awsprddbs4836.shared.sydney.edu.au"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

'''
Validate staff based on username and password
'''
def checkStaffLogin(staffID, password):

    curs = openConnection().cursor()
    query = f"SELECT * FROM staff WHERE staffID = '{staffID}' and password = '{password}'"
    curs.execute(query)
    row = curs.fetchall()
    curs.close()
    if row == []:
        return None
    return list(row[0])

print(checkStaffLogin('jwalker','876'))
'''
List all the associated menu items in the database by staff
'''
def findMenuItemsByStaff(staffID):
    # Establish a database connection and create a cursor
    curs = openConnection().cursor()

    # Query to select menu items reviewed by the given staff member
    query = f"""
            SELECT * 
            FROM MenuItem 
            WHERE Reviewer = '{staffID}'
            """

    # Execute the query
    curs.execute(query)

    # Fetch all the rows
    rows = curs.fetchall()
    if rows == []:
        return None

    # Close the cursor
    curs.close()

    # Return the list of menu items reviewed by the staff member
    return rows

'''
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

'''





'''
Find a list of menu items based on the searchString provided as parameter
See assignment description for search specification
'''
def findMenuItemsByCriteria(searchString):
    # Establish a database connection and create a cursor
    curs = openConnection().cursor()

    # Query to select menu items based on name or description containing the search string
    query = f"""
            SELECT * 
            FROM MenuItem 
            WHERE Name ILIKE '%{searchString}%' OR Description ILIKE '%{searchString}%'
            """

    # Execute the query
    curs.execute(query)

    # Fetch all the rows
    rows = curs.fetchall()

    # Close the cursor
    curs.close()

    # Return the list of menu items matching the search criteria
    return rows



'''
Add a new menu item
'''
def addMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price):
    # Establish a database connection and create a cursor
    conn = openConnection()
    curs = conn.cursor()

    # Query to insert a new menu item into the MenuItem table
    query = f"""
            INSERT INTO MenuItem (Name, Description, CategoryOne, CategoryTwo, CategoryThree, CoffeeType, MilkKind, Price)
            VALUES ('{name}', '{description}', {categoryone}, {categorytwo}, {categorythree}, {coffeetype}, {milkkind}, {price})
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



'''
Update an existing menu item
'''
def updateMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):
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






