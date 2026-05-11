# Database connection and query functions for the Conference Management Application.
# Handles MySQL database operations including attendee, company, session, and room management.
#
# References:
# PyMySQL Documentation: https://pymysql.readthedocs.io/en/latest/
# MySQL Documentation: https://dev.mysql.com/doc/
#
# Development Note:
# Core functionality and error handling was developed with reference to lecture materials.
# Troubleshooting and debugging support was assisted using OpenAI ChatGPT.

import pymysql

conn = None

# SQL database connection approach was adapted from the lecture 10 materials
# The connection is established when needed and closed at the end of the program
def connect():
    global conn
    conn = pymysql.connect(host="localhost",
                        user="root",
                        password="root",
                        db="appdbproj",
                        cursorclass=pymysql.cursors.DictCursor
                        )

def close_connection():
    global conn
    if conn:
        conn.close()
        conn = None

def view_speakers_sessions(speaker_name):
    global conn
    
    if conn is None:
        connect()

    query = """select speakerName, sessionTitle, roomName
    from session s 
    join room r on s.roomId = r.roomId
    where speakerName like %s
    order by speakerName;"""

    with conn.cursor() as cursor:
        # MySQL parameterised queries used to prevent SQL injection
        # Resource: https://pymysql.readthedocs.io/en/latest/modules/cursors.html#pymysql.cursors.Cursor.execute
        cursor.execute(query,(f"%{speaker_name}%",)) 
        results = cursor.fetchall()
        return results

def view_attendees_by_company(company_id):
    global conn
    
    if conn is None:
        connect()
    
    query1 = """select companyName 
    from company where companyID = %s;"""

    # Double %% used because PyMySQL interprets % as Python formatting characters
    # MySQL documentation on date formatting: https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-format
    query2 = """select a.attendeeName, DATE_FORMAT(a.attendeeDOB, '%%Y-%%c-%%e') as attendeeDOB, s.sessionTitle, s.speakerName, s.sessionDate, rm.roomName
    from attendee a
    join registration r on a.attendeeID = r.attendeeID
    join session s on r.sessionID = s.sessionID
    join room rm on rm.roomID = s.roomID
    where attendeeCompanyID = %s
    order by attendeeName;"""

    with conn.cursor() as cursor:
        # Company name
        cursor.execute(query1, (company_id,))
        company = cursor.fetchone()

        # Attendees
        cursor.execute(query2, (company_id,))
        attendees = cursor.fetchall()

    return company, attendees


# Function to validate user input if the company ID exists in the database
def check_company_id_exists(company_id):
    global conn
    
    if conn is None:
        connect()
    
    query = """select companyID, companyName from company where companyID = %s;"""

    with conn.cursor() as cursor:
        cursor.execute(query, (company_id,))
        result = cursor.fetchone()
        return result is not None


# Function to check if a company has any attendees
def check_company_has_attendees(company_id):
    global conn

    if conn is None:
        connect()

    query = """select companyName, count(a.attendeeID) as attendeeCount 
    from company c 
    left join attendee a on a.attendeeCompanyID = c.companyID
    where c.companyID = %s
    group by c.companyName;"""

    with conn.cursor() as cursor:
        cursor.execute(query, (company_id,))
        result = cursor.fetchone()
        return result
    
def add_attendee(attendee_id, name, dob, gender, company_id):
    global conn

    if conn is None:
        connect()

    query = """insert into attendee (attendeeID, attendeeName, attendeeDOB, attendeeCompanyID, attendeeGender) 
    values (%s, %s, %s, %s, %s);"""
    
    # Database error handling for duplicate attendee ID, invalid data, and operational errors
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (attendee_id, name, dob, company_id, gender))
            conn.commit()
            return True
    except pymysql.err.IntegrityError as e:
        print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
        return False
    except pymysql.err.DataError as e:
        print(f"*** ERROR *** {e}")
        return False
    except pymysql.err.OperationalError as e:
        print(f"*** ERROR *** {e}")
        return False

def check_attendee_id_exists(attendee_id):
    global conn

    if conn is None:
        connect()

    query = """select attendeeID from attendee where attendeeID = %s;"""

    with conn.cursor() as cursor:
        cursor.execute(query, (attendee_id,))
        result = cursor.fetchone()
        return result is not None


def get_attendee_name(attendee_id):
    global conn

    if conn is None:
        connect()

    query = """
    select attendeeName 
    from attendee where attendeeID = %s;""" 

    with conn.cursor() as cursor:
        cursor.execute(query, (attendee_id,))
        results = cursor.fetchone()
        if results:
            return results['attendeeName']
        else:
            return results
        
def view_rooms():
    global conn

    if conn is None:
        connect()

    query = """select roomID, roomName, capacity 
    from room
    order by capacity desc;"""

    with conn.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        return results