import requests
import json

data = {
  "career_application": {
    "name": "Mihir Kulshreshtha",
    "email": "mk2664@cornell.edu",
    "role": "Junior Web Developer",
    "notes": "Relationships and community mean everything to me, and I make sure to show up as a positive, present contributor in every group I'm a part of, whether that's been on basketball, dance, or software development teams.",
    "submission_url": "https://windborne-satellite-tracker.onrender.com/",
    "portfolio_url": "https://github.com/EmergenceAI/embodied-drone-agents",
    "resume_url": "https://drive.google.com/file/d/1b5D3AuRW1F7_nae6YI--eCmyo2mll1cr/view?usp=sharing",
  }
} 

url = "https://windbornesystems.com/career_applications.json"
response = requests.post( url=url, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")