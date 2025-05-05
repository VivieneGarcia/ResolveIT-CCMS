from main import Resident, Testing, Testing_Register, CATEGORIES, Authority, User, CSVManager


test_user = Resident(user_id=0, name="Viviene", email="vivs@gmail.com", password="vivi")
Test = Testing(test_user)


test_authority = Authority(user_id=3, name="Princess", email="princess@gmail.com", password="princess")
test_authority  = Testing(test_authority)


def run_test_cases(label, test_cases, method):
    print(f"\n=== Running Tests for '{label}' ===")
    for i, test in enumerate(test_cases, start=1):
        result = method(**test["input"])
        status = "✔" if result == test["expected"] else "✘"
        outcome = "Passed" if status == "✔" else f"Failed: Expected '{test['expected']}', Got '{result}'"
        print(f"[{status}] Test Case {i}: {outcome}")


def test_submit_complaint():
    test_cases = [
        # Happy Path - Valid complaint submission
        {"input": {"category_choice": "1", "title": "Flooded area", "location": "Corner of 3rd and Pine", "description": "Severe flooding after rainfall.", "media": None}, 
        "expected": "✅ Complaint submitted successfully"},

        # Invalid Input Case - Nonexistent category
        {"input": {"category_choice": "99", "title": "Streetlight broken", "location": "5th Avenue", "description": "No lighting at night.", "media": None}, 
        "expected": "❗ Invalid category."},

        # Edge Case - Max title length allowed
        {"input": {"category_choice": "1", "title": "x" * 50, "location": "Main street", "description": "Garbage not collected.", "media": None},
        "expected": "✅ Complaint submitted successfully"}
    ]
    run_test_cases("Submit Complaint", test_cases, Test.test_submit_complaint)


def test_edit_complaint():
    test_cases = [
        # Happy Path - Edit existing complaint
        {"input": {"comp_id": 1, "new_title": "Updated title", "new_category": "2", "new_location": "New location", "new_description": "Updated description", "new_media": None}, 
        "expected": "✅ Complaint updated successfully"},

        # Invalid Input Case - Nonexistent complaint ID
        {"input": {"comp_id": 999, "new_title": "Updated title", "new_category": "2", "new_location": "New location", "new_description": "Updated description", "new_media": None}, 
        "expected": "❌ Complaint not found or Invalid choice."},

    ]
    run_test_cases("Edit Complaint", test_cases, Test.test_edit_complaint)


def test_resolve_complaint():
    test_cases = [
        # Happy Path - Complaint resolved
        {"input": {"complaint_number": 3}, 
        "expected": "✅ Complaint resolved successfully."},

        # Invalid Input - Nonexistent complaint number
        {"input": {"complaint_number": 999}, 
        "expected": "❌ Invalid selection. Please try again."}
    ]
    run_test_cases("Resolve Complaint", test_cases, test_authority.test_resolve_complaint)


def test_reject_complaint():
    test_cases = [
        # Happy Path - Complaint rejected
        {"input": {"complaint_number": 3, "rejection_reason": "Invalid claim."}, 
        "expected": "🚫 Complaint rejected successfully."},

        # Invalid complaint number
        {"input": {"complaint_number": 999, "rejection_reason": "Invalid claim."}, 
        "expected": "❌ Invalid choice. Please select a valid complaint number."},

        # Invalid Empty rejection reason
        {"input": {"complaint_number": 3, "rejection_reason": ""}, 
        "expected": "⚠️ Rejection reason cannot be empty."}
    ]
    run_test_cases("Reject Complaint", test_cases, test_authority.test_reject_complaint)


def test_request_details():
    test_cases = [
        # Happy Path - Valid detail request
        {"input": {"complaint_number": 1, "detail_request": "Please provide a photo of the issue."}, 
        "expected": "🔔 Request for more details has been sent."},

        # Invalid complaint number
        {"input": {"complaint_number": 999, "detail_request": "Need location update."}, 
        "expected": "❌ Invalid choice. Please select a valid complaint number."},

        # Edge Case - Empty detail request
        {"input": {"complaint_number": 1, "detail_request": ""}, 
        "expected": "⚠️ Detail request cannot be empty."}
    ]
    run_test_cases("Request Details", test_cases, test_authority.test_request_details)


def test_user_registration():
    tester = Testing_Register()
    test_cases = [
        # Happy Path - Successful register (no same username)
        {"input": {"username": "newuser", "role": "Resident", "full_name": "John Doe", "email": "john.doe@example.com", "password": "password123"}, 
        "expected": "Registration successful"},

        # Prerequisite: Username already exists
        {"input": {"username": "newuser", "role": "Resident", "full_name": "Jane Doe", "email": "jane.doe@example.com", "password": "password456"}, 
        "expected": "Username already exists"},

        # Invalid Input - Role not among accepted values
        {"input": {"username": "newuser2", "role": "Manager", "full_name": "Alice Smith", "email": "alice.smith@example.com", "password": "password789"}, 
        "expected": "Invalid role"}
    ]
    run_test_cases("User Registration", test_cases, tester.simulate_register)


if __name__ == "__main__":
    test_submit_complaint()
    test_edit_complaint()
    test_resolve_complaint()
    test_reject_complaint()
    test_request_details()
    test_user_registration()
