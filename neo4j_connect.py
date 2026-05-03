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