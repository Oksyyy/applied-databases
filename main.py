import datetime
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
            while True:
                company_id = input("Enter company ID : ")

                if company_id.isdigit() and int(company_id) > 0:
                    if not db_connect.check_company_id_exists(int(company_id)):
                        print(f"Company with ID {company_id} doesn't exist.")
                        continue

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
            print("Add New Attendee")
            print("----------------")
            try:
                attendee_id = int(input("Attendee ID : "))
                name = input("Name : ")
                dob =  datetime.datetime.strptime(input("DOB : "), "%Y-%m-%d")
                gender = input("Gender : ")
                company_id = int(input("Company ID : "))

                # Validate attendee exists
                if db_connect.check_attendee_id_exists(attendee_id):
                    print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
                    return

                # Validate gender input
                elif gender not in ['Male', 'Female']:
                    print("*** ERROR *** Gender must be Male/Female")
                    return

                # Validate company exists
                elif not db_connect.check_company_id_exists(int(company_id)):
                    print(f"*** ERROR *** Company ID: {company_id} does not exist")
                    return

                db_connect.add_attendee(attendee_id, name, dob, gender, company_id)
                print(f"Attendee successfully added")

            # Any other exceptions that may occur
            except Exception as e:
                print({e})
                # print(f"An error occurred: {e}")

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
