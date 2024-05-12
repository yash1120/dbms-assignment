#!/usr/bin/env python3
import psycopg2
import datetime

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

def addMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price):
    # Establish a database connection and create a cursor
    conn = openConnection()
    curs = conn.cursor()
    try :
        query = f"CALL addMenuItem('{name}', '{description}', '{categoryone}', '{categorytwo}', '{categorythree}', '{coffeetype}', '{milkkind}', {price})"
        curs.execute(query)
        #curs.callproc('addmenuitem', (name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price,))
        conn.commit()
        return True
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        curs.close()
        conn.close()



"""
Update an existing menu item
"""


def updateMenuItem(menuitem_id, name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):
    conn = openConnection()
    curs = conn.cursor()
    try :
        query = f"CALL updatemenuitem({menuitem_id}, '{name}', '{description}', '{categoryone}', '{categorytwo}', '{categorythree}', '{coffeetype}', '{milkkind}', {price}, '{reviewdate}', '{reviewer}')"
        curs.execute(query)
        conn.commit()
        return True
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        curs.close()
        conn.close()
    
