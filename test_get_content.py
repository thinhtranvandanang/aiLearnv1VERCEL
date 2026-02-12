#!/usr/bin/env python3
"""
Test getting test content
"""

import requests
import json

def test_get_content():
    """Test getting test content after generation"""
    
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
            
            # Step 1: Generate a test
            test_data = {
                "subject": "Toán học",
                "topic": "Đạo hàm", 
                "level": "easy",
                "question_count": 2
            }
            
            print(f"📝 Generating test...")
            response = requests.post(
                "http://localhost:8000/api/v1/practice-tests/generate",
                json=test_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                test_id = result["data"]["test_id"]
                print(f"✅ Test generated with ID: {test_id}")
                
                # Step 2: Get test content
                print(f"📖 Getting test content...")
                response = requests.get(
                    f"http://localhost:8000/api/v1/practice-tests/{test_id}/content",
                    headers=headers
                )
                
                print(f"📊 Status: {response.status_code}")
                print(f"📊 Response: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "success":
                        content = result["data"]
                        print(f"✅ Test content retrieved!")
                        print(f"   Title: {content['title']}")
                        print(f"   Questions: {content['question_count']}")
                        print(f"   First question: {content['questions'][0]['content'][:100]}...")
                    else:
                        print(f"❌ Error: {result.get('message')}")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
            else:
                print(f"❌ Test generation failed: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_get_content()
