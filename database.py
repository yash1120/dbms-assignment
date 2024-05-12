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
        category = rows[i][3]
        option = rows[i][4]
        price = rows[i][5]
        reviewdate = rows[i][6]
        reviewer = rows[i][7]
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
    conn = openConnection()
    curs = conn.cursor()
    try:
        curs.callproc('check_staff_login', (staffID, password,))
        result = curs.fetchall()
        print(result)
        if result == []:
            return None
        return result[0]
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        curs.close()
        conn.close()


"""
List all the associated menu items in the database by staff
"""


def findMenuItemsByStaff(staffID):
    # Establish a database connection and create a cursor
    try:
        conn = openConnection()
        curs = conn.cursor()
        curs.callproc('viewingmenuitemlist', (staffID,))
        result = curs.fetchall()
        formatted_result = formatMenuItems(result)
        return formatted_result
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        curs.close()
        conn.close()


"""
Find a list of menu items based on the searchString provided as parameter
See assignment description for search specification
"""


def findMenuItemsByCriteria(searchString):
    # Establish a database connection and create a cursor
    conn = openConnection()
    curs = conn.cursor()
    try:
        curs.callproc('findingmenuitems', (searchString,))
        result = curs.fetchall()
        formatted_result = formatMenuItems(result)
        return formatted_result
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        curs.close()
        conn.close()
    


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


def checkLength(value, length):
    if len(value) > length:
        return False
    return True




def addMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price):
    # Establish a database connection and create a cursor
    conn = openConnection()
    curs = conn.cursor()
    try :
        curs.callproc('addmenuitem', (name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price,))
        result = curs.fetchall()
        print(result)
        if result is not None:
            return True
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return False

"""
CREATE OR REPLACE FUNCTION addmenuitem(
    a_name VARCHAR(30),
    a_description VARCHAR(150),
    a_categoryOne VARCHAR(10),
    a_categoryTwo VARCHAR(10),
    a_categoryThree VARCHAR(10),
    a_coffeetype VARCHAR(10),
    a_milkkind VARCHAR(10),
    a_price DECIMAL(6,2)
) RETURNS TABLE (
    menuitemid INTEGER,
    name VARCHAR(30),
    description VARCHAR(150),
    categoryone INTEGER,
    categorytwo INTEGER,
    categorythree INTEGER,
    coffeetype INTEGER,
    milkkind INTEGER,
    price DECIMAL(6,2)
) AS $$
BEGIN
    RETURN QUERY
    INSERT INTO menuitem (name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price)
    VALUES (
        INITCAP(TRIM(a_name)), 
        INITCAP(TRIM(a_description)), 
        (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(a_categoryOne))), 
        (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(a_categoryTwo))), 
        (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(a_categoryThree))), 
        (SELECT coffeetypeid FROM coffeetype WHERE coffeetypename = INITCAP(TRIM(a_coffeetype))), 
        (SELECT milkkindid FROM milkkind WHERE milkkindname = INITCAP(TRIM(a_milkkind))), 
        a_price
    )
    RETURNING
        menuitem.menuitemid, 
        menuitem.name, 
        menuitem.description, 
        menuitem.categoryone, 
        menuitem.categorytwo, 
        menuitem.categorythree, 
        menuitem.coffeetype, 
        menuitem.milkkind, 
        menuitem.price;
END;
$$ LANGUAGE plpgsql;


"""






'''



    # Clean and format input data
    categoryone = categoryone.strip().lower().capitalize()
    categorytwo = categorytwo.strip().lower().capitalize()
    categorythree = categorythree.strip().lower().capitalize()
    coffeetype = coffeetype.strip().lower().capitalize()
    milkkind = milkkind.strip().lower().capitalize()
    description = description.strip()

    # Check for required fields
    if not name or not categoryone or not price:
        return False

    # Check if coffee type is provided but milk kind is missing
    if not coffeetype and milkkind:
        return False

    # Validate categories
    for category in [categoryone, categorytwo, categorythree]:
        if category and getCategoryId(category) is None:
            return False

    # Validate coffee type and milk kind
    for item, function in [(coffeetype, getCoffeeTypeId), (milkkind, getMilkKindId)]:
        if item and function(item) is None:
            return False

    # Check length of name and description
    if not checkLength(name, 30) or not checkLength(description, 150):
        return False

    # Format description if empty
    if not description:
        description = None

    # Validate and format price
    try:
        price = round(float(price), 2)
        if price < 0:
            return False
    except ValueError:
        return False
    finally:
        
        curs.close()
        conn.close()


"""
Update an existing menu item
"""


def updateMenuItem(menuitem_id, name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):
    # Establish a database connection and create a cursor
    conn = openConnection()
    curs = conn.cursor()

    # Clean and format input data
    categoryone = categoryone.strip().lower().capitalize()
    categorytwo = categorytwo.strip().lower().capitalize()
    categorythree = categorythree.strip().lower().capitalize()
    coffeetype = coffeetype.strip().lower().capitalize()
    milkkind = milkkind.strip().lower().capitalize()
    description = description.strip()

    # Check for required fields
    if not name or not categoryone or not price:
        return False

    # Check if coffee type is provided but milk kind is missing
    if not coffeetype and milkkind:
        return False

    # Validate categories
    for category in [categoryone, categorytwo, categorythree]:
        if category and getCategoryId(category) is None:
            return False

    # Validate coffee type and milk kind
    for item, function in [(coffeetype, getCoffeeTypeId), (milkkind, getMilkKindId)]:
        if item and function(item) is None:
            return False

    # Check length of name and description
    if not checkLength(name, 30) or not checkLength(description, 150):
        return False

    # Format description if empty
    if not description:
        description = None

    # Validate and format price
    try:
        price = round(float(price), 2)
        if price < 0:
            return False
    except ValueError:
        return False

    # Construct query
    query = f"""
            UPDATE MenuItem 
            SET Description = '{description}', 
                CategoryOne = {getCategoryId(categoryone)}, 
                CategoryTwo = {getCategoryId(categorytwo) if categorytwo else "NULL"}, 
                CategoryThree = {getCategoryId(categorythree) if categorythree else "NULL"}, 
                CoffeeType = {getCoffeeTypeId(coffeetype) if coffeetype else "NULL"}, 
                MilkKind = {getMilkKindId(milkkind) if milkkind else "NULL"}, 
                Price = {price}, 
                ReviewDate = '{reviewdate}', 
                Reviewer = '{reviewer}'
            WHERE ID = {menuitem_id}
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
