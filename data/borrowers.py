# data/borrowers.py
# 50 NetCredit borrower profiles

import random

borrowers = [
    {"id": "B-1001", "name": "James Wilson",    "credit_score": 720, "monthly_income": 6000,  "loan_amount": 10000, "has_bankruptcy": False, "employment": "Full-time, 5 years"},
    {"id": "B-1002", "name": "Sarah Johnson",   "credit_score": 580, "monthly_income": 3500,  "loan_amount": 8000,  "has_bankruptcy": False, "employment": "Part-time, 1 year"},
    {"id": "B-1003", "name": "Michael Brown",   "credit_score": 490, "monthly_income": 2000,  "loan_amount": 15000, "has_bankruptcy": True,  "employment": "Self-employed, 2 years"},
    {"id": "B-1004", "name": "Emily Davis",     "credit_score": 750, "monthly_income": 8000,  "loan_amount": 12000, "has_bankruptcy": False, "employment": "Full-time, 7 years"},
    {"id": "B-1005", "name": "David Martinez",  "credit_score": 630, "monthly_income": 4500,  "loan_amount": 9000,  "has_bankruptcy": False, "employment": "Full-time, 3 years"},
    {"id": "B-1006", "name": "Jennifer Taylor", "credit_score": 510, "monthly_income": 2800,  "loan_amount": 7000,  "has_bankruptcy": True,  "employment": "Part-time, 6 months"},
    {"id": "B-1007", "name": "Robert Anderson", "credit_score": 700, "monthly_income": 5500,  "loan_amount": 11000, "has_bankruptcy": False, "employment": "Full-time, 4 years"},
    {"id": "B-1008", "name": "Lisa Thomas",     "credit_score": 560, "monthly_income": 3200,  "loan_amount": 6000,  "has_bankruptcy": False, "employment": "Contract, 2 years"},
    {"id": "B-1009", "name": "William Jackson", "credit_score": 810, "monthly_income": 12000, "loan_amount": 20000, "has_bankruptcy": False, "employment": "Full-time, 10 years"},
    {"id": "B-1010", "name": "Mary White",      "credit_score": 470, "monthly_income": 1800,  "loan_amount": 5000,  "has_bankruptcy": True,  "employment": "Unemployed"},
    {"id": "B-1011", "name": "Charles Harris",  "credit_score": 690, "monthly_income": 5000,  "loan_amount": 9500,  "has_bankruptcy": False, "employment": "Full-time, 3 years"},
    {"id": "B-1012", "name": "Patricia Clark",  "credit_score": 540, "monthly_income": 3000,  "loan_amount": 7500,  "has_bankruptcy": False, "employment": "Part-time, 2 years"},
    {"id": "B-1013", "name": "Christopher Lewis","credit_score": 760, "monthly_income": 9000, "loan_amount": 15000, "has_bankruptcy": False, "employment": "Full-time, 8 years"},
    {"id": "B-1014", "name": "Barbara Robinson","credit_score": 620, "monthly_income": 4200,  "loan_amount": 8500,  "has_bankruptcy": False, "employment": "Full-time, 2 years"},
    {"id": "B-1015", "name": "Daniel Walker",   "credit_score": 480, "monthly_income": 2200,  "loan_amount": 6000,  "has_bankruptcy": True,  "employment": "Self-employed, 1 year"},
    {"id": "B-1016", "name": "Susan Hall",      "credit_score": 730, "monthly_income": 7000,  "loan_amount": 13000, "has_bankruptcy": False, "employment": "Full-time, 6 years"},
    {"id": "B-1017", "name": "Paul Allen",      "credit_score": 590, "monthly_income": 3800,  "loan_amount": 8000,  "has_bankruptcy": False, "employment": "Contract, 1 year"},
    {"id": "B-1018", "name": "Karen Young",     "credit_score": 450, "monthly_income": 1500,  "loan_amount": 4000,  "has_bankruptcy": True,  "employment": "Part-time, 6 months"},
    {"id": "B-1019", "name": "Mark Hernandez",  "credit_score": 780, "monthly_income": 10000, "loan_amount": 18000, "has_bankruptcy": False, "employment": "Full-time, 9 years"},
    {"id": "B-1020", "name": "Nancy King",      "credit_score": 640, "monthly_income": 4800,  "loan_amount": 9000,  "has_bankruptcy": False, "employment": "Full-time, 4 years"},
    {"id": "B-1021", "name": "Steven Wright",   "credit_score": 520, "monthly_income": 2900,  "loan_amount": 7000,  "has_bankruptcy": False, "employment": "Part-time, 1 year"},
    {"id": "B-1022", "name": "Betty Lopez",     "credit_score": 710, "monthly_income": 6500,  "loan_amount": 11000, "has_bankruptcy": False, "employment": "Full-time, 5 years"},
    {"id": "B-1023", "name": "George Hill",     "credit_score": 460, "monthly_income": 1900,  "loan_amount": 5000,  "has_bankruptcy": True,  "employment": "Unemployed"},
    {"id": "B-1024", "name": "Dorothy Scott",   "credit_score": 670, "monthly_income": 5200,  "loan_amount": 10000, "has_bankruptcy": False, "employment": "Full-time, 3 years"},
    {"id": "B-1025", "name": "Kenneth Green",   "credit_score": 550, "monthly_income": 3100,  "loan_amount": 6500,  "has_bankruptcy": False, "employment": "Contract, 2 years"},
    {"id": "B-1026", "name": "Sandra Adams",    "credit_score": 740, "monthly_income": 7500,  "loan_amount": 14000, "has_bankruptcy": False, "employment": "Full-time, 7 years"},
    {"id": "B-1027", "name": "Ronald Baker",    "credit_score": 500, "monthly_income": 2500,  "loan_amount": 6000,  "has_bankruptcy": True,  "employment": "Self-employed, 1 year"},
    {"id": "B-1028", "name": "Ashley Gonzalez", "credit_score": 680, "monthly_income": 5000,  "loan_amount": 10000, "has_bankruptcy": False, "employment": "Full-time, 3 years"},
    {"id": "B-1029", "name": "Donald Nelson",   "credit_score": 430, "monthly_income": 1600,  "loan_amount": 4500,  "has_bankruptcy": True,  "employment": "Unemployed"},
    {"id": "B-1030", "name": "Kimberly Carter", "credit_score": 770, "monthly_income": 9500,  "loan_amount": 16000, "has_bankruptcy": False, "employment": "Full-time, 8 years"},
    {"id": "B-1031", "name": "Anthony Mitchell","credit_score": 610, "monthly_income": 4000,  "loan_amount": 8000,  "has_bankruptcy": False, "employment": "Full-time, 2 years"},
    {"id": "B-1032", "name": "Donna Perez",     "credit_score": 530, "monthly_income": 2700,  "loan_amount": 6500,  "has_bankruptcy": False, "employment": "Part-time, 1 year"},
    {"id": "B-1033", "name": "Kevin Roberts",   "credit_score": 790, "monthly_income": 11000, "loan_amount": 19000, "has_bankruptcy": False, "employment": "Full-time, 10 years"},
    {"id": "B-1034", "name": "Carol Turner",    "credit_score": 560, "monthly_income": 3300,  "loan_amount": 7000,  "has_bankruptcy": False, "employment": "Contract, 2 years"},
    {"id": "B-1035", "name": "Brian Phillips",  "credit_score": 440, "monthly_income": 1700,  "loan_amount": 4000,  "has_bankruptcy": True,  "employment": "Unemployed"},
    {"id": "B-1036", "name": "Ruth Campbell",   "credit_score": 720, "monthly_income": 6800,  "loan_amount": 12000, "has_bankruptcy": False, "employment": "Full-time, 5 years"},
    {"id": "B-1037", "name": "Timothy Parker",  "credit_score": 580, "monthly_income": 3600,  "loan_amount": 7500,  "has_bankruptcy": False, "employment": "Part-time, 2 years"},
    {"id": "B-1038", "name": "Sharon Evans",    "credit_score": 650, "monthly_income": 4900,  "loan_amount": 9500,  "has_bankruptcy": False, "employment": "Full-time, 4 years"},
    {"id": "B-1039", "name": "Jason Edwards",   "credit_score": 490, "monthly_income": 2100,  "loan_amount": 5500,  "has_bankruptcy": True,  "employment": "Self-employed, 1 year"},
    {"id": "B-1040", "name": "Deborah Collins", "credit_score": 760, "monthly_income": 8500,  "loan_amount": 14000, "has_bankruptcy": False, "employment": "Full-time, 7 years"},
    {"id": "B-1041", "name": "Ryan Stewart",    "credit_score": 570, "monthly_income": 3400,  "loan_amount": 7000,  "has_bankruptcy": False, "employment": "Contract, 1 year"},
    {"id": "B-1042", "name": "Vamsi Sadam",     "credit_score": 680, "monthly_income": 5000,  "loan_amount": 10000, "has_bankruptcy": False, "employment": "Full-time, 3 years"},
    {"id": "B-1043", "name": "Priya Sharma",    "credit_score": 725, "monthly_income": 7000,  "loan_amount": 12000, "has_bankruptcy": False, "employment": "Full-time, 5 years"},
    {"id": "B-1044", "name": "Ravi Kumar",      "credit_score": 540, "monthly_income": 3000,  "loan_amount": 8000,  "has_bankruptcy": False, "employment": "Part-time, 1 year"},
    {"id": "B-1045", "name": "Anita Patel",     "credit_score": 800, "monthly_income": 11000, "loan_amount": 18000, "has_bankruptcy": False, "employment": "Full-time, 9 years"},
    {"id": "B-1046", "name": "Raj Mehta",       "credit_score": 460, "monthly_income": 1800,  "loan_amount": 5000,  "has_bankruptcy": True,  "employment": "Unemployed"},
    {"id": "B-1047", "name": "Deepa Nair",      "credit_score": 690, "monthly_income": 5500,  "loan_amount": 10500, "has_bankruptcy": False, "employment": "Full-time, 4 years"},
    {"id": "B-1048", "name": "Arjun Singh",     "credit_score": 510, "monthly_income": 2600,  "loan_amount": 6000,  "has_bankruptcy": False, "employment": "Contract, 1 year"},
    {"id": "B-1049", "name": "Meera Reddy",     "credit_score": 750, "monthly_income": 8000,  "loan_amount": 13000, "has_bankruptcy": False, "employment": "Full-time, 6 years"},
    {"id": "B-1050", "name": "Suresh Iyer",     "credit_score": 420, "monthly_income": 1500,  "loan_amount": 4000,  "has_bankruptcy": True,  "employment": "Unemployed"},
]

# Quick decision function — used by dashboard
def quick_decision(borrower):
    score = borrower["credit_score"]
    bankruptcy = borrower["has_bankruptcy"]
    income = borrower["monthly_income"]
    dti = (borrower["loan_amount"] / 12) / income if income > 0 else 99

    if bankruptcy or score < 500 or income < 2000:
        return "REJECT"
    elif score >= 700 and dti < 0.4:
        return "APPROVE"
    else:
        return "REVIEW"