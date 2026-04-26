import db_connect

def main(): # create a function to dysplay menu options for a user to pick and enter
    db_connect.connect()

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
        
        choice = input("Choice: ") # prompt a user to enter their selected choice

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
            db_connect.view_attendees_by_company()

        elif choice == '3':
            db_connect.add_attendee()

        elif choice == '4':
            db_connect.view_connected_attendees()

        elif choice == '5':
            db_connect.add_attendee_connection()

        elif choice == '6':
            db_connect.view_rooms()

        elif choice != 'x':
            print("Please select either 1, 2, 3, 4, 5, or 6")

        db_connect.close_connection()

if __name__ =="__main__":
    main()  
