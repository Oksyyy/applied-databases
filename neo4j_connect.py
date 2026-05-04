from neo4j import GraphDatabase

driver = None

def connect():
    global driver
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, 
                                  auth=("neo4j", "neo4jneo4j"), 
                                  max_connection_lifetime=1000
                                  )

def _connected_attendees(tx, attendee_id):
    query ="""
    MATCH (a:Attendee{AttendeeID:$attendee_id})-[:CONNECTED_TO]-(b:Attendee) 
    RETURN b.AttendeeID as attendeeID 
    ORDER BY b.AttendeeID
    """
    attendees = []
    results = tx.run(query, attendee_id=attendee_id)
    for record in results:
        attendees.append(record["attendeeID"])
    return attendees

def get_connected_attendees_list(attendee_id):
    global driver

    if driver is None:
        connect()

    with driver.session() as session:
        return session.execute_read(_connected_attendees, attendee_id)

def _attendee_exists(tx, attendee_id):
    query = """
    MATCH (a:Attendee {AttendeeID: $attendee_id})
    RETURN count(a) AS count
    """
    result = tx.run(query, attendee_id=attendee_id).single()
    return result["count"] > 0

def check_attendee_exists(attendee_id):
    global driver

    if driver is None:
        connect()

    with driver.session() as session:
        return session.execute_read(_attendee_exists, attendee_id)
    
def _connection_exists(tx, attendee_id_1, attendee_id_2):
    query = """
    MATCH (a:Attendee {AttendeeID: $attendee_id_1})-[r:CONNECTED_TO]-(b:Attendee {AttendeeID: $attendee_id_2})
    RETURN count(r) AS count
    """
    result = tx.run(query, attendee_id_1=attendee_id_1, attendee_id_2=attendee_id_2).single()
    return result["count"] > 0

def check_connection_exists(attendee_id_1, attendee_id_2):
    global driver

    if driver is None:
        connect()

    with driver.session() as session:
        return session.execute_read(_connection_exists, attendee_id_1, attendee_id_2)

def _create_attendee(tx, attendee_id):
    query = """
    CREATE (a:Attendee {AttendeeID: $attendee_id})
    """
    tx.run(query, attendee_id=attendee_id)

def add_attendee(attendee_id):
    global driver

    if driver is None:
        connect()
    
    with driver.session() as session:
        session.execute_write(_create_attendee, attendee_id)

def _create_connection(tx, attendee1, attendee2):
    query = """
    MATCH (a:Attendee {AttendeeID: $attendee_id_1})
    MATCH (b:Attendee {AttendeeID: $attendee_id_2})
    CREATE (a)-[:CONNECTED_TO]->(b)
    """
    tx.run(query, attendee_id_1=attendee1, attendee_id_2=attendee2)


def add_attendee_connection(attendee1, attendee2):
    global driver

    if driver is None:
        connect()
    
    with driver.session() as session:
        session.execute_write(_create_connection, attendee1, attendee2)

    