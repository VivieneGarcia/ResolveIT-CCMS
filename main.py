import csv
import datetime
from typing import Dict, List

class CSVManager:
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


        users_db[username] = user
        CSVManager.save_users(users_db)


        return user


class Resident(User):
    """Residents can submit, edit, and view complaints."""
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, "Resident", password)


    def submit_complaint(self, complaint):
        self.complaints.append(complaint)
        all_complaint.append(complaint)
        CSVManager.save_complaints(all_complaint)


        # Notify all administrators
        for user in users_db.values():
            if user.role == "Administrator":
                NotificationManager.send_notification(
                   sender_id=self.get_user_id(),          
                    recipient_id=user.get_user_id(),        
                    message=f"New complaint (ID: {complaint.get_complaint_id()}) has been submitted by {self.name}."
                )


    def edit_complaint(self, complaint, new_title=None, new_category=None, new_location=None, new_description=None, new_media=None):
        if complaint in self.complaints:
            if new_title: complaint.title = new_title
            if new_category: complaint.category = new_category
            if new_location: complaint.location = new_location
            if new_description: complaint.description = new_description
            if new_media is not None: complaint.media = new_media
            complaint.status = "Assigned"
            print(f"Complaint '{complaint.get_complaint_id()}' updated by {self.name}.")
            CSVManager.save_complaints(all_complaint)
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


        NotificationManager.send_notification(sender_id=user.get_user_id(), recipient_id=authority.get_user_id(),  
        message=f"New complaint (ID: {complaint.get_complaint_id()}) assigned to you."
   )

        
        NotificationManager.send_notification(sender_id=authority.get_user_id(), recipient_id=complaint.get_user_id(),
            message=f"Your complaint (ID: {complaint.get_complaint_id()}) has been assigned to an authority."
        )


        CSVManager.update_complaint_in_csv(complaint)


    def view_all_complaints(self):
        print("\n📋 All Complaints:")
        for comp in all_complaint:
            assigned_authority_name = "Unassigned"
            print(f"🔎 Checking assigned authority ID: {comp.assigned_authority_id}")  # Debug


            if comp.assigned_authority_id:
                assigned_authority = self.get_authority(comp.assigned_authority_id)
                assigned_authority_name = assigned_authority.name if assigned_authority else "Unknown"


            print("---------------------------------------------------------")
            print(f"🆔 ID: {comp.get_complaint_id()} | User: {comp.get_user_id()}")
            print(f"📝 Title: {comp.title}")
            print(f"🏷️ Category: {comp.category} | 📍 Location: {comp.location}")
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
    """Authorities can resolve, reject complaints, or request more details."""
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, "Authority", password)


    def resolve_complaint(self, complaint):
        complaint.status = "Resolved"
        NotificationManager.send_notification(sender_id=self.get_user_id(),recipient_id=complaint.get_user_id(),            
            message=f"Your complaint (ID: {complaint.get_complaint_id()}) has been resolved by {self.name}."
        )
        CSVManager.save_complaints(all_complaint)


    def reject_complaint(self, complaint, reason):
       complaint.status = "Rejected"
        NotificationManager.send_notification(sender_id=self.get_user_id(),recipient_id=complaint.get_user_id(),  
            message=f"Your complaint (ID: {complaint.get_complaint_id()}) was rejected by {self.name}. Reason: {reason}"
        )
        CSVManager.save_complaints(all_complaint)


    def request_details(self, complaint, detail_request):
        complaint.status = "Pending Details"
        NotificationManager.send_notification(sender_id=self.get_user_id(),recipient_id=complaint.get_user_id(),
            message=f"🔔 {self.name} requests more details for complaint (ID: {complaint.get_complaint_id()}):{detail_request}"
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
                print("---------------------------------------------------------")
                print(f"🆔 ID: {comp.get_complaint_id()} | User: {comp.get_user_id()}")
                print(f"📝 Title: {comp.title}")
                print(f"🏷️ Category: {comp.category} | 📍 Location: {comp.location}")
                print(f"🚦 Status: {comp.status} | ⏰ Timestamp: {comp.timestamp.strftime('%Y-%m-%d %H:%M')}")
                if comp.media:
                    print(f"🔗 Media: {comp.media}")
                print("---------------------------------------------------------")
       
        if not found:
            print("📄 No complaints assigned to you.")
