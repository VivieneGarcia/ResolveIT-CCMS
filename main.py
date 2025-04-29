import csv
import datetime
import os
from typing import Dict, List

CATEGORIES = {
    "1": "🔊 Noise",
    "2": "🗑️ Garbage",
    "3": "🚦 Traffic",
    "4": "🎨 Vandalism",
    "5": "🚰 Water Supply",
    "6": "💡 Street Light",
    "7": "❓ Other"
}

class Testing:
    def __init__(self, user):
        self.user = user
        self.next_complaint_id = 1
        self.user.complaints = CSVManager.load_complaints()
        
    def test_submit_complaint(self, category_choice, title, location, description, media=None):
        global next_complaint_id

        if category_choice not in CATEGORIES:
            return "❗ Invalid category."
        if not title or len(title) > 50:
            return "❗ Invalid title."
        if not location or len(location) > 120:
            return "❗ Invalid location."
        if not description:
            return "❗ Invalid description."

        category = CATEGORIES[category_choice]
        timestamp = datetime.datetime.now()
        assigned_authority_id = None

        complaint = Complaint(
            complaint_id=next_complaint_id,
            user_id=user.get_user_id(),
            title=title,
            category=category,
            location=location,
            description=description,
            media=media,
            status="Submitted",
            timestamp=timestamp,
            assigned_authority_id=assigned_authority_id
        )

        self.user.submit_complaint(complaint)
        self.next_complaint_id += 1
        return "✅ Complaint submitted successfully"

    def test_edit_complaint(self, comp_id, new_title, new_category, new_location, new_description, new_media=None):
        complaint = next((c for c in self.user.complaints if c.get_complaint_id() == comp_id), None)
        
        if not complaint:
            return "❌ Complaint not found or Invalid choice."
        
        if complaint.status.lower() in ["rejected", "resolved"]:
            return "❌ This complaint has been rejected or resolved and cannot be edited."
        
        # Validate new title
        if len(new_title) > 50:
            return f"❗ Title is too long ({len(new_title)} characters). Maximum is 50."
        
        # Validate new location
        if len(new_location) > 120:
            return f"❗ Location is too long ({len(new_location)} characters). Maximum is 120."
        
        # Validate new description
        if not new_description:
            return "❗ Description cannot be empty."
        
        # Update the complaint
        complaint.title = new_title
        complaint.category = new_category
        complaint.location = new_location
        complaint.description = new_description
        complaint.media = new_media
        
        self.user.edit_complaint(complaint, new_title, new_category, new_location, new_description, new_media)
        
        return "✅ Complaint updated successfully"

class CSVManager:
    @staticmethod
    def ensure_csv_files():
        """Ensure that all required CSV files exist with the correct headers."""
        files_with_headers = {
            "users.csv": ['username', 'user_id', 'name', 'email', 'role', 'password'],
            "complaints.csv": ['complaint_id', 'user_id', 'title', 'category', 'location', 
                               'description', 'media', 'status', 'timestamp', 'assigned_authority_id'],
            "notifications.csv": ['sender_id', 'recipient_id', 'message', 'timestamp']
        }

        for file, headers in files_with_headers.items():
            if not os.path.exists(file):
                with open(file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)  # Write the header row
                print(f"✅ Created missing file: {file}")
            else:
                print(f"🔹 {file} already exists.")
                
    @staticmethod
    def load_users() -> Dict[str, 'User']:
        users = {}
        try:
            with open('users.csv', 'r', newline='', encoding='utf-8') as file:
                for row in csv.DictReader(file):
                    user_id, role, username = int(row['user_id']), row['role'], row['username']
                    if role == "Resident": users[username] = Resident(user_id, row['name'], row['email'], row['password'])
                    elif role == "Administrator": users[username] = Administrator(user_id, row['name'], row['email'], row['password'])
                    elif role == "Authority": users[username] = Authority(user_id, row['name'], row['email'], row['password'])
        except FileNotFoundError: pass
        return users

    @staticmethod
    def save_users(users: Dict[str, 'User']):
        with open('users.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'user_id', 'name', 'email', 'role', 'password'])
            for username, user in users.items():
                writer.writerow([username, user.get_user_id(), user.name, user.email, user.role, user._User__password])

    @staticmethod
    def load_complaints():
        complaints = []
        try:
            with open('complaints.csv', 'r', newline='', encoding='utf-8') as file:
                for row in csv.DictReader(file):
                    complaints.append(Complaint(
                        complaint_id=int(row['complaint_id']),
                        user_id=int(row['user_id']),
                        title=row['title'],
                        category=row['category'],
                        location=row['location'],
                        description=row['description'],
                        timestamp=datetime.datetime.fromisoformat(row['timestamp']),
                        media=row['media'] or None,
                        status=row['status'],
                        assigned_authority_id=int(row['assigned_authority_id']) if row['assigned_authority_id'] else None
                    ))
        except FileNotFoundError: pass
        return complaints

    @staticmethod
    def save_complaints(complaints: List['Complaint']):
        with open('complaints.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['complaint_id', 'user_id', 'title', 'category', 'location', 'description', 'media', 'status', 'timestamp', 'assigned_authority_id'])
            for c in complaints:
                writer.writerow([c.get_complaint_id(), c.get_user_id(), c.title, c.category, c.location, c.description,
                                 c.media or '', c.status, c.timestamp.isoformat(), c.assigned_authority_id or ''])
                
    @staticmethod
    def load_notifications():
        notifications = []
        with open('notifications.csv', 'r') as file:
            for row in csv.DictReader(file):
                try: recipient_id = int(row['recipient_id'])
                except ValueError: recipient_id = None
                notifications.append({'sender_id': int(row['sender_id']), 'recipient_id': recipient_id,
                                      'message': row['message'], 'timestamp': row['timestamp']})
        return notifications

    @staticmethod
    def save_notification(notification: dict):
        with open('notifications.csv', 'a', newline='', encoding='utf-8') as file:
            csv.writer(file).writerow([notification['sender_id'], notification['recipient_id'],
                                       notification['message'], notification['timestamp'].isoformat()])
    @staticmethod
    def update_complaint_in_csv(complaint):
        csv_file = "complaints.csv"
        complaints = []
        updated = False


        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames


            for row in reader:
                if row["complaint_id"] == str(complaint.get_complaint_id()):
                    row["status"] = complaint.status
                    row["assigned_authority_id"] = complaint.assigned_authority_id or ""
                    updated = True
                complaints.append(row)


        if updated:
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(complaints)


            print(f"✅ Complaint {complaint.get_complaint_id()} successfully assigned and updated in CSV.")
        else:
            print(f"❌ Complaint {complaint.get_complaint_id()} not found in CSV.")

# print("🔹 Ensuring CSV files exist...")
# CSVManager.ensure_csv_files() 

class User:
    def __init__(self, user_id: int, name: str, email: str, role: str, password: str):
        self.__user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.__password = password

    def login(self, password: str):
        if password == self.__password:
            print(f"✅ User {self.name} logged in successfully.")
            return True
        else:
            print("❌ Invalid password. Access denied.")
            return False

    def logout(self):
        print(f"🚪 User {self.name} has logged out.")

    def get_user_id(self):
        return self.__user_id
   
    def get_password(self):
        return self.__password

    @classmethod
    def register(cls, user_id, username, name, email, role, password, users_db):
        if role == "Resident":
            user = Resident(user_id, name, email, password)
        elif role == "Administrator":
            user = Administrator(user_id, name, email, password)
        elif role == "Authority":
            user = Authority(user_id, name, email, password)
        else:
            return None

        if isinstance(user, Resident):
            user.complaints = [] 
        if isinstance(user, Authority):
            user.assigned_complaints = [] 
            
        users_db[username] = user
        CSVManager.save_users(users_db)

        return user


class Resident(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, "Resident", password)
        self.complaints = []

    def submit_complaint(self, complaint):
        self.complaints.append(complaint)
        all_complaint.append(complaint)
        CSVManager.save_complaints(all_complaint)
        print("✅ Complaint submitted successfully!")

        # Notify all administrators
        for user in users_db.values():
            if user.role == "Administrator":
                NotificationManager.send_notification(
                   sender_id=self.get_user_id(),          
                    recipient_id=user.get_user_id(),        
                    message=f"New complaint (Title: {complaint.title.title()}) has been submitted by {self.name}."
                )

    def edit_complaint(self, complaint, new_title=None, new_category=None, new_location=None, new_description=None, new_media=None):
        if complaint in self.complaints:
            if new_title: complaint.title = new_title
            if new_category: complaint.category = new_category
            if new_location: complaint.location = new_location
            if new_description: complaint.description = new_description
            if new_media is not None: complaint.media = new_media
            CSVManager.save_complaints(all_complaint)
            print("✅ Complaint updated successfully")
            
        else:
            print("You can only edit your own complaints.")
   
    def view_complaints(self):
        print("\n📋 My Complaints")
        print("══════════════════════════════════════════════════════════")

        for comp in self.complaints:
            assigned_authority = self.get_authority(comp.assigned_authority_id)
            assigned_authority_name = assigned_authority.name if assigned_authority else "Unassigned"
            print(f"🆔 ID: {comp.get_complaint_id()} | 📝 Title: {comp.title}")
            print(f"🏷️ Category: {comp.category} | 📍 Location: {comp.location}")
            print(f"📝 Description: {comp.description}")
            print(f"🚦 Status: {comp.status} | ⏰ Timestamp: {comp.timestamp.strftime('%Y-%m-%d %H:%M')}")
            if comp.media:
                print(f"🔗 Media: {comp.media}")
            print(f"👮 Assigned Authority: {assigned_authority_name}")
            print("---------------------------------------------------------")
        print("══════════════════════════════════════════════════════════")
       
    def get_authority(self, user_id):
        for user in users_db.values():  
            if str(user.get_user_id()) == str(user_id):
                return user
        return None

class Administrator(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, "Administrator", password)

    def assign_complaint(self, complaint, authority):
        complaint.status = "Assigned"
        complaint.assigned_authority_id = authority.get_user_id()
        authority.assigned_complaints.append(complaint)

        NotificationManager.send_notification(sender_id=self.get_user_id(), recipient_id=authority.get_user_id(),  
        message=f"New complaint (Title: {complaint.title.title()}) assigned to you."
   )

        NotificationManager.send_notification(sender_id=authority.get_user_id(), recipient_id=complaint.get_user_id(),
            message=f"Your complaint (Title: {complaint.title.title()}) has been assigned to an authority."
        )


        CSVManager.update_complaint_in_csv(complaint)

    def view_all_complaints(self):
        print("\n📋 All Complaints:")
        for comp in all_complaint:
            assigned_authority_name = "Unassigned"

            if comp.assigned_authority_id:
                assigned_authority = self.get_authority(comp.assigned_authority_id)
                assigned_authority_name = assigned_authority.name if assigned_authority else "Unknown"

            user = next(
                (u for u in users_db.values() if getattr(u, '_User__user_id', None) == comp.get_user_id()),
                None
            )

            user_name_display = user.name if user else f"Unknown (ID: {comp.get_user_id()})"

            print("---------------------------------------------------------")
            print(f"🆔 ID: {comp.get_complaint_id()} | 👤 User: {user_name_display}")
            print(f"📝 Title: {comp.title}")
            print(f"🏷️ Category: {comp.category} | 📍 Location: {comp.location}")
            print(f"📝 Description: {comp.description}")
            print(f"🚦 Status: {comp.status} | ⏰ Timestamp: {comp.timestamp.strftime('%Y-%m-%d %H:%M')}")
            if comp.media:
                print(f"🔗 Media: {comp.media}")
            print(f"👮 Assigned Authority: {assigned_authority_name}")
            print("---------------------------------------------------------")

    def get_authority(self, user_id):
        for user in users_db.values():
            if str(user.get_user_id()) == str(user_id):
                return user
        print("🚫 User not found.")
        return None

class Authority(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, "Authority", password)

    def resolve_complaint(self, complaint):
        complaint.status = "Resolved"
        NotificationManager.send_notification(sender_id=self.get_user_id(),recipient_id=complaint.get_user_id(),            
            message=f"Your complaint (Title: {complaint.title.title()}) has been resolved by {self.name}."
        )
        CSVManager.save_complaints(all_complaint)

    def reject_complaint(self, complaint, reason):
        complaint.status = "Rejected"
        NotificationManager.send_notification(sender_id=self.get_user_id(),recipient_id=complaint.get_user_id(),  
            message=f"Your complaint (Title: {complaint.title.title()}) was rejected by {self.name}. Reason: {reason}"
        )
        CSVManager.save_complaints(all_complaint)

    def request_details(self, complaint, detail_request):
        complaint.status = "Pending Details"
        NotificationManager.send_notification(sender_id=self.get_user_id(),recipient_id=complaint.get_user_id(),
            message=f"🔔 {self.name} requests more details for complaint (Title: {complaint.title.title()}):{detail_request}"
        )
        CSVManager.save_complaints(all_complaint)
   
    def view_assigned_complaints(self):
        """Displays all complaints assigned to this authority."""
        print(f"\n📋 Assigned Complaints for {self.name}:")
        found = False  # To check if there are any assigned complaints
        
        for comp in all_complaint:
            # Check if the complaint is assigned to this authority
            if comp.assigned_authority_id == self.get_user_id():
                found = True
                
                # Find the user who submitted the complaint
                user = next(
                    (u for u in users_db.values() if getattr(u, '_User__user_id', None) == comp.get_user_id()),
                    None
                )
                
                # Display the user's name if found, otherwise show the ID
                user_display = user.name if user else f"User ID: {comp.get_user_id()}"
                
                print("---------------------------------------------------------")
                print(f"🆔 ID: {comp.get_complaint_id()} | 👤 User: {user_display}")
                print(f"📝 Title: {comp.title}")
                print(f"🏷️ Category: {comp.category} | 📍 Location: {comp.location}")
                print(f"📝 Description: {comp.description}")
                print(f"🚦 Status: {comp.status} | ⏰ Timestamp: {comp.timestamp.strftime('%Y-%m-%d %H:%M')}")
                if comp.media:
                    print(f"🔗 Media: {comp.media}")
                print("---------------------------------------------------------")
        
        if not found:
            print("📄 No complaints assigned to you.")

class Complaint:
    def __init__(self, complaint_id, user_id, title, category, location, description, media, status, timestamp, assigned_authority_id):
        self.__complaint_id = complaint_id
        self.__user_id = user_id
        self.title = title
        self.category = category
        self.location = location
        self.description = description
        self.media = media
        self.status = status
        self.timestamp = timestamp
        self.assigned_authority_id = assigned_authority_id

    def get_complaint_id(self):
        return self.__complaint_id  

    def get_user_id(self):
        return self.__user_id

class NotificationManager:
    notifications_db = CSVManager.load_notifications()
    @classmethod
    def send_notification(cls, sender_id: int, recipient_id: int, message: str):
        notification = {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "message": message,
            "timestamp": datetime.datetime.now()
        }
        cls.notifications_db.append(notification)
        CSVManager.save_notification(notification)
        print(f"🔔 Notification sent to user {recipient_id}")

    @classmethod
    def view_notifications(cls, user_id: int):
        notifications = [n for n in cls.notifications_db if n['recipient_id'] == user_id]
        if not notifications:
            print("📭 No new notifications")
            return
        print("\n📨 Notifications:")
        for idx, notif in enumerate(notifications, 1):
            timestamp = notif['timestamp']
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    print(f"⚠️ Invalid timestamp format: {timestamp}")
                    continue
            print(f"{idx}. [{timestamp.strftime('%m/%d %H:%M')}] {notif['message']}")

users_db = CSVManager.load_users()
all_complaint = CSVManager.load_complaints()

for user in users_db.values():
    if isinstance(user, Resident):
        user.complaints = [c for c in all_complaint if c.get_user_id() == user.get_user_id()]
    if isinstance(user, Authority):
        user.assigned_complaints = [c for c in all_complaint if c.assigned_authority_id == user.get_user_id()]

next_user_id = max((u.get_user_id() for u in users_db.values()), default=0) + 1
next_complaint_id = max((c.get_complaint_id() for c in all_complaint), default=0) + 1

def main():
    global next_user_id, next_complaint_id
    while True:
        print("\n🏢 RESOLVEIT: Community Complaint Management System")
        print("🔐 [1] Login")
        print("📝 [2] Register")
        print("❌ [3] Exit")
        choice = input("\n👉 Enter choice: ").strip()

        if choice == '1': handle_login()
        elif choice == '2': handle_register()
        elif choice == '3': break
        else: print("❌ Invalid choice")

def handle_login():
    username = input("\n📝 Username: ").strip()
    password = input("🔒 Password: ").strip()
    
    user = users_db.get(username)
    if not user or not user.login(password):
        print("❌ Login failed")
        return
    
    if user.role == "Resident": resident_dashboard(user)
    elif user.role == "Administrator": admin_dashboard(user)
    else: authority_dashboard(user)

def handle_register():
    global next_user_id
    print("\n🌟 New Registration")
    username = input("📝 Username: ").strip()

    if username in users_db:
        print("❌ Username already exists. Registration failed.")
        return

    role = input("👤 Role (Resident/Administrator/Authority): ").strip().capitalize()
    if role not in ["Resident", "Administrator", "Authority"]:
        print("❌ Invalid role. Registration failed.")
        return

    user = User.register(next_user_id,username,
        input("📛 Full Name: ").strip(),
        input("📧 Email: ").strip(),role,
        input("🔑 Password: ").strip(),
        users_db
    )
    if user:
        next_user_id += 1
        print("✅ Registration successful!")
        
def resident_dashboard(user: Resident):
    while True:
        print(f"\n🏠 Resident Dashboard: {user.name}")
        print("1. Submit Complaint")
        print("2. Edit Complaint")
        print("3. My Complaints")
        print("4. Notifications")
        print("5. Logout")
        choice = input("\n👉 Enter choice: ").strip()

        if choice == '1': handle_submit_complaint(user)
        elif choice == '2': handle_edit_complaint(user)
        elif choice == '3': user.view_complaints()
        elif choice == '4': NotificationManager.view_notifications(user.get_user_id())
        elif choice == '5': break
        else: print("❌ Invalid choice")

def handle_submit_complaint(user: Resident):
    global next_complaint_id

    print("\n📂 Select a category:")
    for key, value in CATEGORIES.items():
        print(f"[{key}] {value}")

    # Validate category choice
    while True:
        category_choice = input("👉 Enter category number: ").strip()
        if category_choice in CATEGORIES:
            category = CATEGORIES[category_choice]
            break
        else:
            print("❗ Invalid category. Please enter a number from the list.")

    # Validate non-empty title with max 50 characters
    while True:
        title = input("👉 Enter title (max 50 characters): ").strip()
        if not title:
            print("❗ Title cannot be empty. Please enter a valid title.")
        elif len(title) > 50:
            print(f"❗ Title is too long ({len(title)} characters). Maximum is 50.")
        else:
            break

    # Validate non-empty location with max 120 characters
    while True:
        location = input("👉 Enter location (max 120 characters): ").strip()
        if not location:
            print("❗ Location cannot be empty. Please enter a valid location.")
        elif len(location) > 120:
            print(f"❗ Location is too long ({len(location)} characters). Maximum is 120.")
        else:
            break

    # Validate non-empty description
    while True:
        description = input("👉 Enter complaint description: ").strip()
        if not description:
            print("❗ Description cannot be empty. Please enter a valid description.")
        else:
            break

    # Media link (optional)
    media = input("👉 Provide any media link (optional): ").strip() or None

    timestamp = datetime.datetime.now()
    assigned_authority_id = None  

    complaint = Complaint(
        complaint_id=next_complaint_id,
        user_id=user.get_user_id(),
        title=title,
        category=category,
        location=location,
        description=description,
        media=media,
        status="Submitted",
        timestamp=timestamp,
        assigned_authority_id=assigned_authority_id
    )

    user.submit_complaint(complaint)
    next_complaint_id += 1
    

def handle_edit_complaint(resident):
    resident.view_complaints()
    if not resident.complaints:
        print("\n❗ No complaints found!")
        return

    # Show complaints with index numbers
    print("\n📋 Select a complaint to edit:")
    for idx, complaint in enumerate(resident.complaints, start=1):
        print(f"[{idx}] 📝 {complaint.title} | 📍 {complaint.location} | 🚦 {complaint.status}")

    # Choose from numbered list
    while True:
        choice_input = input("➡️ Enter the number of the complaint to edit: ").strip()
        if choice_input.isdigit():
            index = int(choice_input) - 1
            if 0 <= index < len(resident.complaints):
                complaint = resident.complaints[index]
                break
            else:
                print("❌ Invalid choice. Please choose a valid number.")
        else:
            print("❌ Please enter a number.")

    # Prevent editing resolved/rejected complaints
    if complaint.status.lower() in ["rejected", "resolved"]:
        print("❌ This complaint has been rejected or resolved and cannot be edited.")
        return

    print("\n✏️ Edit Complaint (leave blank to keep current value)")

    # Title validation
    while True:
        new_title = input(f"📝 New title ({complaint.title}): ").strip() or complaint.title
        if len(new_title) > 50:
            print(f"❗ Title is too long ({len(new_title)} characters). Maximum is 50.")
        else:
            break

    # Category selection
    print("\n🏷️ Select new category or press Enter to keep current")
    for key, value in CATEGORIES.items():
        print(f"[{key}] {value}")
    while True:
        new_cat_choice = input(f"New category ({complaint.category}): ").strip()
        if new_cat_choice == "" or new_cat_choice in CATEGORIES:
            new_category = CATEGORIES.get(new_cat_choice, complaint.category) if new_cat_choice else complaint.category
            break
        else:
            print("❗ Invalid category. Please enter a number from the list.")

    # Location validation
    while True:
        new_location = input(f"📍 New location ({complaint.location}): ").strip() or complaint.location
        if len(new_location) > 120:
            print(f"❗ Location is too long ({len(new_location)} characters). Maximum is 120.")
        else:
            break

    # Description validation
    while True:
        new_description = input(f"📄 New description ({complaint.description}): ").strip() or complaint.description
        if not new_description:
            print("❗ Description cannot be empty. Please enter a valid description.")
        else:
            break

    # Optional media
    new_media = input(f"📷 New media ({complaint.media}): ").strip() or complaint.media

    # Update complaint
    resident.edit_complaint(complaint, new_title, new_category, new_location, new_description, new_media)


        
def admin_dashboard(admin):
    while True:
        print(f"\n👔 Administrator Dashboard: {admin.name} 👔")
        print("[1] View all complaints 📋")
        print("[2] Assign complaint ➡️")
        print("[3] View notifications 🔔")
        print("[4] Logout 🚪")
        choice = input("\n🌈 Enter your choice: ")

        if choice == '1': admin.view_all_complaints()
        elif choice == '2':handle_assign_complaint(admin)
        elif choice == '3':NotificationManager.view_notifications(admin.get_user_id())
        elif choice == '4':
            admin.logout()
            break
        else:print("\n❌ Invalid choice. Please try again.")
        
def handle_assign_complaint(admin):
    admin.view_all_complaints()
    try:
        comp_id = int(input("\n🆔 Enter complaint ID to assign: "))
        complaint = next((c for c in all_complaint if c.get_complaint_id() == comp_id), None)
        
        if not complaint:
            print("\n❌ Complaint not found!")
            return
            
        print("\n👮 Available Authorities:")
        authorities = [u for u in users_db.values() if u.role == "Authority"]
        for idx, auth in enumerate(authorities, 1):
            print(f"[{idx}] {auth.name}")
            
        auth_choice = int(input("🌈 Select authority: ")) - 1
        if 0 <= auth_choice < len(authorities):
            admin.assign_complaint(complaint, authorities[auth_choice])
        else:
            print("\n❌ Invalid authority selection!")
    except ValueError:
        print("\n❌ Invalid input format!")

def authority_dashboard(authority):
    while True:
        print(f"\n👮 Authority Dashboard: {authority.name} 👮")
        print("[1] View assigned complaints 📋")
        print("[2] Resolve complaint ✅")
        print("[3] Reject complaint ❌")
        print("[4] Request details ❓")
        print("[5] View notifications 🔔")
        print("[6] Logout 🚪")
        choice = input("\n🌈 Enter your choice: ")

        if choice == '1':
            authority.view_assigned_complaints()
        elif choice == '2':
            handle_resolve_complaint(authority)
        elif choice == '3':
            handle_reject_complaint(authority)
        elif choice == '4':
            handle_request_details(authority)
        elif choice == '5':
            NotificationManager.view_notifications(authority.get_user_id())
        elif choice == '6':
            authority.logout()
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

def handle_request_details(authority):
    if not authority.assigned_complaints:
        print("📭 No assigned complaints to request details for.")
        return

    print("\n🔍 Assigned Complaints:")
    for idx, complaint in enumerate(authority.assigned_complaints, 1):
        print(f"{idx}. 🆔 {complaint.get_complaint_id()} | {complaint.title} | Status: {complaint.status}")

    try:
        choice = int(input("\n👉 Enter the number of the complaint to request details for: ")) - 1
        if 0 <= choice < len(authority.assigned_complaints):
            complaint = authority.assigned_complaints[choice]
            detail_request = input("📝 Enter the additional information needed: ").strip()
            authority.request_details(complaint, detail_request)
            print("🔔 Request for more details has been sent.")
        else:
            print("❌ Invalid choice. Please try again.")
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")

def handle_resolve_complaint(authority):
    if not authority.assigned_complaints:
        print("📭 No assigned complaints to resolve.")
        return

    print("📋 Assigned Complaints:")
    for idx, complaint in enumerate(authority.assigned_complaints, 1):
        print(f"{idx}. 🆔 {complaint.get_complaint_id()} | {complaint.title} | Status: {complaint.status}")
    try:
        choice = int(input("\n👉 Enter the number of the complaint to resolve: ")) - 1
        if choice < 0 or choice >= len(authority.assigned_complaints):
            print("❌ Invalid selection. Please try again.")
            return

        complaint = authority.assigned_complaints[choice]
        
        authority.resolve_complaint(complaint)
        print("✅ Complaint resolved successfully.")

    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")

def handle_reject_complaint(authority: Authority):
    if not authority.assigned_complaints:
        print("❌ No assigned complaints to reject.")
        return

    for idx, complaint in enumerate(authority.assigned_complaints, 1):
        print(f"{idx}. 🆔 {complaint.get_complaint_id()} | {complaint.title} | Status: {complaint.status}")

    try:
        choice = int(input("Enter the complaint number to reject: ")) - 1
        complaint = authority.assigned_complaints[choice]
        reason = input("Enter the reason for rejection: ").strip()
        authority.reject_complaint(complaint, reason)
    except (ValueError, IndexError):
        print("❌ Invalid input.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

          
if __name__ == "__main__":
    main()