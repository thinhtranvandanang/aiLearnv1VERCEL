#!/usr/bin/env python3
"""
Test the test generation API
"""

import requests
import json

def test_generate_test():
    """Test the test generation endpoint"""
    
    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        # Login
        response = requests.post("http://localhost:8000/api/v1/auth/student/login", json=login_data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                token = result["data"]["access_token"]
                print(f"✅ Login successful, got token: {token[:50]}...")
                
                # Test generation
                test_data = {
                    "subject": "Toán học",
                    "topic": "Đạo hàm", 
                    "level": "easy",
                    "question_count": 3
                }
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                print(f"📝 Requesting test generation: {test_data}")
                
                response = requests.post(
                    "http://localhost:8000/api/v1/practice-tests/generate",
                    json=test_data,
                    headers=headers
                )
                
                print(f"📊 Response status: {response.status_code}")
                print(f"📊 Response body: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "success":
                        print("🎉 Test generation successful!")
                        print(f"   Test ID: {result['data']['test_id']}")
                        print(f"   Title: {result['data']['title']}")
                    else:
                        print(f"❌ Test generation failed: {result.get('message')}")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    print(f"   Response: {response.text}")
            else:
                print(f"❌ Login failed: {result.get('message')}")
        else:
            print(f"❌ Login HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_generate_test()
