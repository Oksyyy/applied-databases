def main(): # create a function to dysplay menu options for a user to pick and enter
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
            view_speakers_sessions()

        elif choice == '2':
            view_attendees_by_company()

        elif choice == '3':
            add_attendee()

        elif choice == '4':
            view_connected_attendees()

        elif choice == '5':
            add_attendee_connection()

        elif choice == '6':
            view_rooms()

        elif choice != 'x':
            print("Please select either 1, 2, 3, 4, 5, or 6")

if __name__ =="__main__":
    main()  
