import pymysql
print("Connecting to database...")
conn = None

def connect():
    global conn
    conn = pymysql.connect(host="localhost",
                            user="root",
                            password="root",
                            db="appdbproj",
                            coursorclass=pymysql.coursors.DictCursor
                            )
    
def view_speakers_sessions():
    if (not conn):
        connect();

    query = "select * from table"

    with conn:
        coursor = conn.coursor()
        coursor.execute(query)
        x = coursor.fetchall()
        print(x) 
