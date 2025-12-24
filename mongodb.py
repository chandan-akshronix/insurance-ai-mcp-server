from pymongo import MongoClient
from datetime import datetime

# MongoDB connection (adjust connection string as needed)
client = MongoClient("mongodb+srv://Abhijit:RStoKAluIWB4x1Pg@cluster0.zvgvv7n.mongodb.net/")  # or your Atlas URI
db = client["insurance_onboarding_db"]

# Collections
kyc_coll = db["kyc"]
history_coll = db["insurance_history"]
financial_coll = db["financial_eligibility"]
credit_coll = db["credit"]
income_coll = db["income"]
medical_coll = db["medical"]

# Sample documents

# 1. KYC record
kyc_doc = {
    "pan_number": "AAAPK1234A",
    "name": "John Doe",
    "date_of_birth": "1980-01-15",
    "verification_time": datetime.utcnow(),
    "verification_status": "VERIFIED",
    "uid_token": "UIDTKN_xyz123",
    "consent": {
        "timestamp": "2025-11-20T10:00:00Z",
        "ip_address": "203.0.113.45"
    }
}

# 2. Insurance history record
history_doc = {
    "applicant": {
        "name": "John Doe",
        "date_of_birth": "1980-01-15",
        "pan_number": "AAAPK1234A",
        "idType": "PAN"
    },
    "previousPolicies": [
        {
            "carrier": "ABC Insurance Co",
            "policyNumber": "POL123456",
            "policyType": "Motor",
            "effectiveDate": "2020-04-01",
            "expiryDate": "2021-04-01",
            "status": "Expired",
            "sumAssured": 5000000,
            "numberOfClaims": 1,
            "totalClaimsAmount": 25000.00,
            "continuousCoverageMonths": 12
        }
    ],
    "summary": {
        "hasPreviousCoverage": True,
        "coverageLapseMonths": 0,
        "claimsInLast12Months": 1,
        "underwritingFlag": "refer"
    },
    "requestContext": {
        "purpose": "underwritingEligibility",
        "consent": {
            "timestamp": "2025-11-20T11:00:00Z",
            "ipAddress": "203.0.113.45"
        }
    }
}

# 3. Financial eligibility record
financial_doc = {
    "applicant": {
        "name": "John Doe",
        "dateOfBirth": "1980-01-15",
        "pan_number": "AAAPK1234A",
        "idType": "PAN"
    },
    "employment": {
        "employerName": "ABC Corp",
        "employmentType": "Salaried",
        "monthlyIncome": 85000
    },
    "financials": {
        "annualIncome": 1020000,
        "existingLiabilities": 250000,
        "assets": [
            {"type": "RealEstate", "value": 5000000},
            {"type": "Investments", "value": 300000}
        ]
    },
    "requestContext": {
        "purpose": "insuranceFinancialUnderwriting",
        "sumAssured": 2000000,
        "premiumMode": "Annual",
        "consent": {
            "timestamp": "2025-11-20T12:00:00Z",
            "ipAddress": "203.0.113.45"
        }
    },
    "financialVerification": {
        "incomeVerified": True,
        "incomeToSumAssuredRatio": 0.51,
        "premiumToIncomeRatio": 0.09
    },
    "underwritingInsight": {
        "riskScore": 72,
        "recommendation": "Accept",
        "notes": "Income sufficient for requested cover; liabilities within acceptable range"
    }
}

# 4. Credit record
credit_doc = {
    "pan_number": "AAAPK1234A",
    "creditScore": 745,
    "bureau": "CIBIL",
    "report": {
        "creditAccountsSummary": {
            "activeAccounts": 3,
            "closedAccounts": 1,
            "totalAccounts": 4
        },
        "paymentHistory": {
            "monthsPaidOnTime": 35,
            "monthsDelayed": 2,
            "defaultStatus": "No"
        },
        "creditUtilization": 35,
        "inquiries": 2,
        "negativeMarks": 0
    }
}

# 5. Income record
income_doc = {
    "pan_number": "AAAPK1234A",
    "employment": {
        "employerName": "ABC Corp",
        "employmentType": "Salaried",
        "designation": "Senior Manager",
        "yearsOfService": 8,
        "monthlyIncome": 85000
    },
    "financials": {
        "annualIncome": 1020000,
        "taxableIncome": 950000,
        "netIncome": 900000,
        "otherIncome": 50000
    },
    "verification": {
        "verified": True,
        "verificationDate": "2025-11-20",
        "source": "ITRDocument",
        "documents": ["ITR", "SalarySlip", "BankStatement"]
    }
}

# 6. Medical record
medical_doc = {
    "pan_number": "AAAPK1234A",
    "medicalHistory": [
        {
            "condition": "Hypertension",
            "diagnosisDate": "2020-03-15",
            "status": "Controlled",
            "medications": ["Lisinopril"]
        },
        {
            "condition": "Diabetes",
            "diagnosisDate": "2019-06-20",
            "status": "Controlled",
            "medications": ["Metformin"]
        }
    ],
    "healthStatus": {
        "bloodPressure": "130/85",
        "bloodGlucose": 145,
        "BMI": 26.5,
        "lastCheckupDate": "2025-11-15",
        "smokingStatus": "Non-smoker"
    },
    "report": {
        "medicalExamDate": "2025-11-18",
        "examinedBy": "Dr. Smith",
        "overallAssessment": "Fit with conditions",
        "recommendations": ["Regular monitoring", "Follow-up after 6 months"]
    }
}

# Insert documents
kyc_result = kyc_coll.insert_one(kyc_doc)
print("Inserted KYC ID:", kyc_result.inserted_id)

history_result = history_coll.insert_one(history_doc)
print("Inserted Insurance History ID:", history_result.inserted_id)

financial_result = financial_coll.insert_one(financial_doc)
print("Inserted Financial Eligibility ID:", financial_result.inserted_id)

credit_result = credit_coll.insert_one(credit_doc)
print("Inserted Credit ID:", credit_result.inserted_id)

income_result = income_coll.insert_one(income_doc)
print("Inserted Income ID:", income_result.inserted_id)

medical_result = medical_coll.insert_one(medical_doc)
print("Inserted Medical ID:", medical_result.inserted_id)

# --- Test Data for User Request (EMAPB9558L) ---
# Cloning the structure for the new PAN
pan_test = "EMAPB9558L"

kyc_test = kyc_doc.copy()
kyc_test["pan_number"] = pan_test
kyc_test["name"] = "Test Applicant"

history_test = history_doc.copy()
history_test["applicant"]["pan_number"] = pan_test

financial_test = financial_doc.copy()
financial_test["applicant"]["pan_number"] = pan_test

credit_test = credit_doc.copy()
credit_test["pan_number"] = pan_test

income_test = income_doc.copy()
income_test["pan_number"] = pan_test

medical_test = medical_doc.copy()
medical_test["pan_number"] = pan_test

print(f"\n--- Seeding Data for {pan_test} ---")
db["kyc"].insert_one(kyc_test)
db["insurance_history"].insert_one(history_test)
db["financial_eligibility"].insert_one(financial_test)
db["credit"].insert_one(credit_test)
db["income"].insert_one(income_test)
db["medical"].insert_one(medical_test)
print("Seeding complete for EMAPB9558L.")
