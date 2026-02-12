#!/usr/bin/env python3
"""
Test full flow: generate test -> submit -> get results
"""

import requests
import json

def test_full_flow():
    """Test complete flow from test generation to results"""
    
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
            
            print(f"\n📝 Step 1: Generating test...")
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
                print(f"\n📖 Step 2: Getting test content...")
                response = requests.get(
                    f"http://localhost:8000/api/v1/practice-tests/{test_id}/content",
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    questions = result["data"]["questions"]
                    print(f"✅ Got {len(questions)} questions")
                    
                    # Step 3: Submit answers
                    print(f"\n📤 Step 3: Submitting answers...")
                    answers = {}
                    for i, q in enumerate(questions):
                        # Simple logic: alternate between A and B
                        answer = "A" if i % 2 == 0 else "B"
                        answers[str(q["id"])] = answer
                    
                    submit_data = {
                        "answers": answers,
                        "start_time": "2025-01-01T10:00:00Z",
                        "end_time": "2025-01-01T10:30:00Z"
                    }
                    
                    response = requests.post(
                        f"http://localhost:8000/api/v1/practice-tests/{test_id}/submit-online",
                        json=submit_data,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        submission_id = result["data"]["submission_id"]
                        print(f"✅ Submitted with submission ID: {submission_id}")
                        
                        # Step 4: Get results
                        print(f"\n📊 Step 4: Getting results...")
                        response = requests.get(
                            f"http://localhost:8000/api/v1/submissions/{submission_id}/result",
                            headers=headers
                        )
                        
                        print(f"📊 Status: {response.status_code}")
                        print(f"📊 Response: {response.text}")
                        
                        if response.status_code == 200:
                            result = response.json()
                            if result.get("status") == "success":
                                data = result["data"]
                                print(f"✅ Results retrieved!")
                                print(f"   Score: {data['score']}")
                                print(f"   Correct: {data['correct_answers']}/{data['total_questions']}")
                            else:
                                print(f"❌ Error: {result.get('message')}")
                        else:
                            print(f"❌ HTTP Error: {response.status_code}")
                    else:
                        print(f"❌ Submit failed: {response.text}")
                else:
                    print(f"❌ Get content failed: {response.text}")
            else:
                print(f"❌ Test generation failed: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_full_flow()
