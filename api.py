from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Abhijit:RStoKAluIWB4x1Pg@cluster0.zvgvv7n.mongodb.net/")
DB_NAME = os.getenv("DB_NAME", "insurance_onboarding_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

app = FastAPI(title="Insurance Onboarding API")

# Helper to convert ObjectId to str
def transform_doc(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# Example schema classes
class KYCRecord(BaseModel):
    pan_number: str
    name: str
    date_of_birth: str
    verification_status: str
    uid_token: Optional[str]
    consent: Optional[dict]

class InsuranceHistoryRecord(BaseModel):
    applicant: dict
    previousPolicies: List[dict]
    summary: dict
    requestContext: dict

class FinancialEligibilityRecord(BaseModel):
    applicant: dict
    employment: dict
    financials: dict
    requestContext: dict
    financialVerification: dict
    underwritingInsight: dict

class CreditRecord(BaseModel):
    pan_number: str
    creditScore: int
    bureau: str
    report: dict

class IncomeRecord(BaseModel):
    pan_number: str
    employment: dict
    financials: dict
    verification: dict

class MedicalRecord(BaseModel):
    pan_number: str
    medicalHistory: List[dict]
    healthStatus: dict
    report: dict

# Endpoints
@app.get("/kyc/{pan_number}", response_model=KYCRecord)
def get_kyc(pan_number: str):
    coll = db["kyc"]
    doc = coll.find_one({"pan_number": pan_number})
    if not doc:
        raise HTTPException(status_code=404, detail="KYC record not found")
    return transform_doc(doc)

@app.get("/insurance-history/{pan_number}", response_model=InsuranceHistoryRecord)
def get_insurance_history(pan_number: str):
    coll = db["insurance_history"]
    doc = coll.find_one({"applicant.pan_number": pan_number})
    if not doc:
        raise HTTPException(status_code=404, detail="Insurance history record not found")
    return transform_doc(doc)

@app.get("/financial-eligibility/{pan_number}", response_model=FinancialEligibilityRecord)
def get_financial_eligibility(pan_number: str):
    coll = db["financial_eligibility"]
    doc = coll.find_one({"applicant.pan_number": pan_number})
    if not doc:
        raise HTTPException(status_code=404, detail="Financial eligibility record not found")
    return transform_doc(doc)

@app.get("/credit/{pan_number}", response_model=CreditRecord)
def get_credit(pan_number: str):
    coll = db["credit"]
    doc = coll.find_one({"pan_number": pan_number})
    if not doc:
        raise HTTPException(status_code=404, detail="Credit record not found")
    return transform_doc(doc)

@app.get("/income/{pan_number}", response_model=IncomeRecord)
def get_income(pan_number: str):
    coll = db["income"]
    doc = coll.find_one({"pan_number": pan_number})
    if not doc:
        raise HTTPException(status_code=404, detail="Income record not found")
    return transform_doc(doc)

@app.get("/medical/{pan_number}", response_model=MedicalRecord)
def get_medical(pan_number: str):
    coll = db["medical"]
    doc = coll.find_one({"pan_number": pan_number})
    if not doc:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return transform_doc(doc)

@app.get("/")
def read_root():
    return {"message": "Insurance Onboarding API"}

