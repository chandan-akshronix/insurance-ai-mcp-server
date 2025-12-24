from pymongo import MongoClient
import os

MONGO_URI = "mongodb+srv://Abhijit:RStoKAluIWB4x1Pg@cluster0.zvgvv7n.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["insurance_onboarding_db"]

pan = "EMAPB9558L"

# Update Insurance History to add sumAssured
result = db["insurance_history"].update_one(
    {"applicant.pan_number": pan},
    {
        "$set": {
            "previousPolicies.$[].sumAssured": 5000000
        }
    }
)

print(f"Updated {result.modified_count} documents for PAN {pan}.")

# Verify
doc = db["insurance_history"].find_one({"applicant.pan_number": pan})
if doc:
    print("Verification: First policy sumAssured =", doc.get("previousPolicies", [{}])[0].get("sumAssured"))
else:
    print("Error: Document not found!")
