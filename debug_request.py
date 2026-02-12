#!/usr/bin/env python3
"""
Debug script to check what frontend is sending
"""

import requests
import json

def debug_frontend_request():
    """Debug what the frontend might be sending"""
    
    # Test different question_count values that frontend might send
    test_cases = [
        {"subject": "Toán học", "topic": "Đạo hàm", "level": "easy", "question_count": 5},
        {"subject": "Toán học", "topic": "Đạo hàm", "level": "easy", "question_count": 10},
        {"subject": "Toán học", "topic": "Đạo hàm", "level": "medium", "question_count": 5},
        {"subject": "Vật lý", "topic": "Sóng cơ", "level": "hard", "question_count": 2},  # This should fail
    ]
    
    # Login to get token
    login_data = {"username": "testuser", "password": "test123"}
    
    try:
        response = requests.post("http://localhost:8000/api/v1/auth/student/login", json=login_data)
        if response.status_code == 200:
            result = response.json()
            token = result["data"]["access_token"]
            print(f"✅ Got token: {token[:50]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            for i, test_data in enumerate(test_cases, 1):
                print(f"\n🧪 Test case {i}: {test_data}")
                
                response = requests.post(
                    "http://localhost:8000/api/v1/practice-tests/generate",
                    json=test_data,
                    headers=headers
                )
                
                print(f"📊 Status: {response.status_code}")
                print(f"📊 Response: {response.text}")
                
                if response.status_code == 400:
                    result = response.json()
                    if "Hiện có:" in result.get("message", ""):
                        print(f"❌ Not enough questions available")
                    else:
                        print(f"❌ Other 400 error: {result.get('message')}")
                elif response.status_code == 200:
                    print(f"✅ Success!")
                    
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_frontend_request()
