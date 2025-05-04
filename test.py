from main import Resident, Testing, CATEGORIES, Authority, Complaint
import datetime

test_user = Resident(user_id=0, name="Viviene", email="vivs@gmail.com", password="vivi")
Test = Testing(test_user)


# Create a test authority (with complaints assigned)
test_authority = Authority(user_id=3, name="Princess", email="princess@gmail.com", password="princess")
# Create a test authority (without complaints assigned)
test_authority  = Testing(test_authority )

def run_test_cases(label, test_cases, method):
    print(f"\nRunning tests for '{label}'...\n")
    for i, test in enumerate(test_cases, start=1):
        result = method(**test["input"])
        if result == test["expected"]:
            print(f"✅ Test Case {i} Passed")
        else:
            print(f"❌ Test Case {i} Failed: Expected '{test['expected']}', Got '{result}'")


def test_submit_complaint():
    test_cases = [
        # Happy Path
        {
            "input": {
                "category_choice": "1",
                "title": "Flooded area",
                "location": "Corner of 3rd and Pine",
                "description": "Severe flooding after rainfall.",
                "media": None
            },
            "expected": "✅ Complaint submitted successfully"
        },
        # Invalid Input Case
        {
            "input": {
                "category_choice": "99",
                "title": "Streetlight broken",
                "location": "5th Avenue",
                "description": "No lighting at night.",
                "media": None
            },
            "expected": "❗ Invalid category."
        },
        # Edge Case
        {
            "input": {
                "category_choice": "1",
                "title": "x" * 50,
                "location": "Main street",
                "description": "Garbage not collected.",
                "media": None
            },
            "expected": "✅ Complaint submitted successfully"
        }
    ]
    run_test_cases("Submit Complaint", test_cases, Test.test_submit_complaint)


def test_edit_complaint():
    test_cases = [
        # Happy Path
        {
            "input": {
                "comp_id": 1,
                "new_title": "Updated title",
                "new_category": "2",
                "new_location": "New location",
                "new_description": "Updated description",
                "new_media": None
            },
            "expected": "✅ Complaint updated successfully"
        },
        # Invalid Input Case
        {
            "input": {
                "comp_id": 999,
                "new_title": "Updated title",
                "new_category": "2",
                "new_location": "New location",
                "new_description": "Updated description",
                "new_media": None
            },
            "expected": "❌ Complaint not found or Invalid choice."
        },
        # Edge Case
        {
            "input": {
                "comp_id": 1,
                "new_title": "x" * 51,
                "new_category": "2",
                "new_location": "New location",
                "new_description": "Updated description",
                "new_media": None
            },
            "expected": "❗ Title is too long (51 characters). Maximum is 50."
        }
    ]
    run_test_cases("Edit Complaint", test_cases, Test.test_edit_complaint)

def test_resolve_complaint():
    test_cases = [
        # Happy Path: Complaint resolved
        {
            "input": {"complaint_number": 3},
            "expected": "✅ Complaint resolved successfully."
        },
        # Invalid complaint number
        {
            "input": {"complaint_number": 999},
            "expected": "❌ Invalid selection. Please try again."
        }
    ]
    run_test_cases("Resolve Complaint", test_cases, test_authority.handle_resolve_complaint)

def test_reject_complaint():
    test_cases = [
        # Happy Path: Complaint rejected
        {
            "input": {"complaint_number": 3, "rejection_reason": "Invalid claim."},
            "expected": "🚫 Complaint rejected successfully."
        },
        # Invalid complaint number
        {
            "input": {"complaint_number": 999, "rejection_reason": "Invalid claim."},
            "expected": "❌ Invalid choice. Please select a valid complaint number."
        },
        # Empty rejection reason
        {
            "input": {"complaint_number":3, "rejection_reason": ""},
            "expected": "⚠️ Rejection reason cannot be empty."
        }
    ]
    run_test_cases("Reject Complaint", test_cases, test_authority.handle_reject_complaint)

def test_request_details():
    test_cases = [
        # Happy Path
        {
            "input": {"authority": test_authority.user, "complaint_number": 1, "detail_request": "Please provide a photo of the issue."},
            "expected": "🔔 Request for more details has been sent."
        },
        # Invalid complaint number
        {
            "input": {"authority": test_authority.user, "complaint_number": 999, "detail_request": "Need location update."},
            "expected": "❌ Invalid choice. Please select a valid complaint number."
        },
        # Empty detail request
        {
            "input": {"authority": test_authority.user, "complaint_number": 1, "detail_request": ""},
            "expected": "⚠️ Detail request cannot be empty."
        }
    ]
    run_test_cases("Request Details", test_cases, test_authority.handle_request_details)

if __name__ == "__main__":
    test_submit_complaint()
    test_edit_complaint()
    test_resolve_complaint()
    test_reject_complaint()
    test_request_details()
