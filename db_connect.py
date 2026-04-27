from unittest import result

import pymysql
print("Connecting to database...")
conn = None

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
        cursor.execute(query,(f"%{speaker_name}%",))
        results = cursor.fetchall()
        return results

def view_attendees_by_company(company_id):
    global conn
    
    if conn is None:
        connect()
    
    query1 = """select companyName 
    from company where companyID = %s;"""

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

    query = """select companyName, count(a.attendeeID) as attendeeCount from company c 
    left join attendee a on a.attendeeCompanyID = c.companyID
    where c.companyID = %s;"""

    with conn.cursor() as cursor:
        cursor.execute(query, (company_id,))
        result = cursor.fetchone()
        return result