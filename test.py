from main import Resident, Testing, CATEGORIES

test_user = Resident(user_id=0, name="Viviene", email="vivs@gmail.com", password="vivi")
Test = Testing(test_user)

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


if __name__ == "__main__":
    test_submit_complaint()
    test_edit_complaint()
