import db_connect
import neo4j_connect

# Create a function to display menu options for a user to pick and enter
def main(): 
    db_connect.connect()

    # Initialize rooms variable to store room data for menu: choice 6 to avoid multiple database calls
    rooms = None

    choice = ""

    while choice != 'x':
        print("Conference Management")
        print("---------------------\n")
        print("MENU")
        print("====")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("x - Exit application")
        
        # Prompt a user to enter their selected choice
        choice = input("Choice: ")

        if choice == '1':
            speaker_name = input("\nEnter speaker name : ")
            results = db_connect.view_speakers_sessions(speaker_name)
            print(f"Session Details For : {speaker_name}")
            print("---------------------------------------------------")
            if not results:
                print("No speakers found of that name")
            else:
                for speakers in results:
                    print(f"{speakers['speakerName']} | {speakers['sessionTitle']} | {speakers['roomName']}")

        elif choice == '2':
            while True:
                # Validate company ID input is an integer
                try: 
                    company_id = int(input("\nEnter company ID : "))
                except ValueError:
                    continue

                # Validate company ID is a positive integer
                if company_id > 0:
                    if not db_connect.check_company_id_exists(int(company_id)):
                        print(f"Company with ID {company_id} doesn't exist.")
                        continue
                    
                    # Validate company has attendees
                    company_data = db_connect.check_company_has_attendees(int(company_id))
                    if company_data['attendeeCount'] == 0:
                        print(f"{company_data['companyName']} Attendees")
                        print(f"No attendees found for {company_data['companyName']}")
                        continue
                    
                    break
            company, attendees = db_connect.view_attendees_by_company(company_id)
            print(f"{company['companyName']} Attendees")
            for attendee in attendees:
                print(f"{attendee['attendeeName']} | {attendee['attendeeDOB']} | {attendee['sessionTitle']} | {attendee['speakerName']} | {attendee['sessionDate']} | {attendee['roomName']}")

        elif choice == '3':
            print("\nAdd New Attendee")
            print("----------------")
            attendee_id = input("Attendee ID : ")
            name = input("Name : ")
            dob =  input("DOB : ")
            gender = input("Gender : ")
            company_id = int(input("Company ID : "))

            # Validate attendee exists
            if db_connect.check_attendee_id_exists(attendee_id):
                print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
                continue

            # Validate gender input
            elif gender not in ['Male', 'Female']:
                print("*** ERROR *** Gender must be Male/Female")
                continue

            # Validate company exists
            elif not db_connect.check_company_id_exists(int(company_id)):
                print(f"*** ERROR *** Company ID: {company_id} does not exist")
                continue

            success = db_connect.add_attendee(attendee_id, name, dob, gender, company_id)
            if success:
                print(f"Attendee successfully added\n")

        elif choice == '4':
            while True:
                # Validate attendee ID input is an integer
                try:
                    attendee_id = int(input("\nEnter Attendee ID : "))
                except ValueError:
                    print("*** ERROR *** Invalid attendee ID")
                    continue
                    
                # Check if attendee exists in Neo4j
                attendee_id = int(attendee_id)
                if not db_connect.check_attendee_id_exists(attendee_id):
                    print("*** ERROR *** Attendee does not exist")
                    continue
                break
            
            print(f"Attendee Name: {db_connect.get_attendee_name(attendee_id)}")
            print("------------------------------")
            connected_ids = neo4j_connect.get_connected_attendees_list(attendee_id)
            # Check if there are any connections for an attendee
            if (len(connected_ids) == 0):
                print("No connections")
            else:
                print("These attendees are connected: ")
                for connected_id in connected_ids:
                    name = db_connect.get_attendee_name(connected_id)
                    print(f"{connected_id} | {name}")

        elif choice == '5':
            while True:
                attendee_id_1 = input("\nEnter Attendee 1 ID : ")
                attendee_id_2 = input("Enter Attendee 2 ID : ")
                # Validate attendee ID inputs are integers
                try:
                    attendee_id_1 = int(attendee_id_1)
                    attendee_id_2 = int(attendee_id_2)
                except ValueError:
                    print("*** ERROR *** Attendee IDs must be numbers")
                    continue
                
                # Check if attendee IDs are the same
                if attendee_id_1 == attendee_id_2:
                    print( "*** ERROR *** An attendee cannot connect to him/herself")
                    continue

                # Check if attendee IDs exist in SQL database
                if not db_connect.check_attendee_id_exists(attendee_id_1):
                    print(f"*** ERROR *** One or both attendee IDs do not exist")
                    continue

                if not db_connect.check_attendee_id_exists(attendee_id_2):
                    print(f"*** ERROR *** One or both attendee IDs do not exist")
                    continue

                 # Add attendees to Neo4j if missing
                if not neo4j_connect.check_attendee_exists(attendee_id_1):
                    neo4j_connect.add_attendee(attendee_id_1)

                if not neo4j_connect.check_attendee_exists(attendee_id_2):
                    neo4j_connect.add_attendee(attendee_id_2)
                
                # Check if attendees are already connected
                if neo4j_connect.check_connection_exists(attendee_id_1, attendee_id_2):
                    print(f"*** ERROR *** These attendees are already connected")
                    continue

                break

            neo4j_connect.add_attendee_connection(attendee_id_1, attendee_id_2)
            print(f"Attendee {attendee_id_1} is now connected to Attendee {attendee_id_2}")

        elif choice == '6':
            if rooms is None:
                rooms = db_connect.view_rooms()
            print("RoomID | Room Name | Capacity")
            for room in rooms:
                print(f"{room['roomID']} | {room['roomName']} | {room['capacity']}")

        elif choice != 'x':
            print("Please select either 1, 2, 3, 4, 5, or 6")

    db_connect.close_connection()
    neo4j_connect.close_connection()

if __name__ =="__main__":
    main()  
