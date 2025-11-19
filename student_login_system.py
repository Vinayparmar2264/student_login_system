import json
import os
import sys

DATA_FILE = "students.json"

students = {}       # dictionary: username -> profile dict
logged_user = ""    # empty string means no one is logged in

def load_students():
    """Load students from DATA_FILE into the students dict.
       If file doesn't exist, start with empty dictionary."""
    global students
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            text = f.read()
            if text.strip() == "":
                students = {}
            else:
                students = json.loads(text)
    else:
        students = {}

def save_students():
    """Save the students dictionary to DATA_FILE as JSON text."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        text = json.dumps(students, indent=2)  # convert dict to nice JSON text
        f.write(text)

def wait():
    """Pause so user can read messages."""
    input("\nPress Enter to continue...")

def register():
    """Register a new student. Collect at least 10 fields."""
    global students
    print("\n--- REGISTER ---")
    # choose username
    while True:
        username = input("Enter username (no spaces): ").strip()
        if username == "":
            print("Username cannot be empty.")
            continue
        if " " in username:
            print("Please do not use spaces.")
            continue
        if username in students:
            print("This username already exists. Pick another.")
            continue
        break
    # password
    while True:
        password = input("Enter password: ")
        password2 = input("Confirm password: ")
        if password != password2:
            print("Passwords do not match.")
            continue
        if len(password) < 4:
            print("Password too short (min 4).")
            continue
        break

    print("\nEnter the student details (press Enter to leave a field blank):")
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    gender = input("Gender(M/F/O): ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    address = input("Address: ").strip()
    course = input("Course (e.g. B.Tech CS): ").strip()
    year = input("Semester: ").strip()
    roll_no = input("Enrollment  ID: ").strip()
    guardian = input("Guardian name: ").strip()
    extra = input("Any extra info: ").strip()

    profile = {
        "username": username,
        "password": password, 
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob,
        "gender(M/F/O)": gender,
        "email": email,
        "phone": phone,
        "address": address,
        "course": course,
        "year": year,
        "roll_no": roll_no,
        "guardian": guardian,
        "extra": extra
    }

    students[username] = profile
    save_students()
    print("\nRegistration complete. You can now login with your username.")
    wait()

def login():
    """Login by username and password."""
    global logged_user
    print("\n--- LOGIN ---")
    username = input("Username: ").strip()
    if username == "":
        print("Please enter a username.")
        wait()
        return
    if username not in students:
        print("No such user. Register first.")
        wait()
        return
    password = input("Password: ")
    if password == students[username]["password"]:
        logged_user = username
        print("Login successful. Welcome,", students[username].get("first_name", username))
    else:
        print("Wrong password.")
    wait()

def show_profile():
    """Display the profile of the logged-in user."""
    print("\n--- SHOW PROFILE ---")
    if logged_user == "":
        print("You must login first to view profile.")
        wait()
        return
    profile = students.get(logged_user)
    if profile is None:
        print("Profile not found.")
        wait()
        return

    # Print each field except the password
    print("Username :", profile.get("username", ""))
    print("First name:", profile.get("first_name", ""))
    print("Last name :", profile.get("last_name", ""))
    print("DOB       :", profile.get("dob", ""))
    print("Gender    :", profile.get("gender", ""))
    print("Email     :", profile.get("email", ""))
    print("Phone     :", profile.get("phone", ""))
    print("Address   :", profile.get("address", ""))
    print("Course    :", profile.get("course", ""))
    print("Year      :", profile.get("year", ""))
    print("Roll No   :", profile.get("roll_no", ""))
    print("Guardian  :", profile.get("guardian", ""))
    print("Extra     :", profile.get("extra", ""))

    wait()

def update_profile():
    """Update profile fields for the logged-in user (or change password)."""
    global students
    print("\n--- UPDATE PROFILE ---")
    if logged_user == "":
        print("You must login first to update profile.")
        wait()
        return
    profile = students.get(logged_user)
    if profile is None:
        print("Profile missing.")
        wait()
        return

    while True:
        print("\nUpdate options:")
        print("1 - Update fields (name, email, phone, address, etc.)")
        print("2 - Change password")
        print("3 - Back to main menu")
        choice = input("Choose 1/2/3: ").strip()
        if choice == "1":
            nf = input("First name (leave blank to keep): ").strip()
            if nf != "":
                profile["first_name"] = nf
            nl = input("Last name (leave blank to keep): ").strip()
            if nl != "":
                profile["last_name"] = nl
            ne = input("Email (leave blank to keep): ").strip()
            if ne != "":
                profile["email"] = ne
            np = input("Phone (leave blank to keep): ").strip()
            if np != "":
                profile["phone"] = np
            na = input("Address (leave blank to keep): ").strip()
            if na != "":
                profile["address"] = na
            nc = input("Course (leave blank to keep): ").strip()
            if nc != "":
                profile["course"] = nc
            ny = input("Year (leave blank to keep): ").strip()
            if ny != "":
                profile["year"] = ny
            ng = input("Guardian (leave blank to keep): ").strip()
            if ng != "":
                profile["guardian"] = ng
            ne2 = input("Extra info (leave blank to keep): ").strip()
            if ne2 != "":
                profile["extra"] = ne2

            students[logged_user] = profile
            save_students()
            print("Profile updated.")
            wait()
        elif choice == "2":
            old = input("Enter current password: ")
            if old != profile["password"]:
                print("Current password is wrong.")
                wait()
            else:
                new1 = input("Enter new password: ")
                new2 = input("Confirm new password: ")
                if new1 != new2:
                    print("Passwords do not match.")
                elif len(new1) < 4:
                    print("New password is too short.")
                else:
                    profile["password"] = new1
                    students[logged_user] = profile
                    save_students()
                    print("Password changed.")
                wait()
        elif choice == "3":
            break
        else:
            print("Please choose 1, 2, or 3.")

def logout():
    """Logout the current logged-in user."""
    global logged_user
    print("\n--- LOGOUT ---")
    if logged_user == "":
        print("No user is logged in.")
    else:
        print("User", logged_user, "has been logged out.")
        logged_user = ""
    wait()

def terminate():
    """Exit the program."""
    print("\nExiting. Goodbye!")
    sys.exit(0)

def main():
    load_students()   
    while True:
        print("\n=== LNCT Student System (Very Simple) ===")
        print("1. Registration")
        print("2. Login")
        print("3. Show Profile")
        print("4. Update Profile")
        print("5. Logout")
        print("6. Main Menu (show again)")
        print("7. Exit")
        choice = input("Select option 1-7: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            show_profile()
        elif choice == "4":
            update_profile()
        elif choice == "5":
            logout()
        elif choice == "6":
            continue  # loop will reprint menu
        elif choice == "7":
            terminate()
        else:
            print("Invalid choice, please enter a number from 1 to 7.")

if __name__ == "__main__":
    main()