import csv
import datetime
from typing import Dict, List

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
