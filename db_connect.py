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