"""
Test script to diagnose file upload issues
"""
import requests
import os

# Test file upload endpoint
API_URL = "http://127.0.0.1:8000"

def test_resume_upload():
    """Test resume upload with a text file"""
    print("=" * 80)
    print("Testing Resume Upload")
    print("=" * 80)
    
    # Create a simple test resume file
    test_content = """
    John Doe
    Software Engineer
    
    Experience:
    - 5 years of Python development
    - Expert in FastAPI and Django
    - AWS cloud infrastructure
    
    Skills:
    Python, JavaScript, React, Docker, Kubernetes
    
    Education:
    BS Computer Science, MIT, 2018
    """
    
    # Save as a text file
    test_file_path = "test_resume.txt"
    with open(test_file_path, "w") as f:
        f.write(test_content)
    
    try:
        # Upload the file
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_resume.txt", f, "text/plain")}
            response = requests.post(f"{API_URL}/upload-resume/", files=files)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("\n✓ Resume upload successful!")
            data = response.json()
            print(f"Resume ID: {data.get('id')}")
        else:
            print("\n✗ Resume upload failed!")
            try:
                error_detail = response.json()
                print(f"Error: {error_detail}")
            except:
                print(f"Raw error: {response.text}")
    
    except Exception as e:
        print(f"\n✗ Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_jd_upload():
    """Test job description upload with a text file"""
    print("\n" + "=" * 80)
    print("Testing Job Description Upload")
    print("=" * 80)
    
    # Create a simple test JD file
    test_content = """
    Senior Software Engineer
    Tech Corp
    
    We are looking for an experienced software engineer to join our team.
    
    Requirements:
    - 5+ years of Python development
    - Experience with FastAPI, Django, or Flask
    - Strong understanding of cloud platforms (AWS, Azure, GCP)
    - Excellent communication skills
    
    Responsibilities:
    - Design and develop scalable applications
    - Lead technical discussions
    - Mentor junior developers
    - Write clean, maintainable code
    """
    
    # Save as a text file
    test_file_path = "test_jd.txt"
    with open(test_file_path, "w") as f:
        f.write(test_content)
    
    try:
        # Upload the file
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_jd.txt", f, "text/plain")}
            data = {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "job_url": "https://example.com/jobs/123"
            }
            response = requests.post(f"{API_URL}/upload-jd/", files=files, data=data)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("\n✓ Job description upload successful!")
            data = response.json()
            print(f"JD ID: {data.get('id')}")
        else:
            print("\n✗ Job description upload failed!")
            try:
                error_detail = response.json()
                print(f"Error: {error_detail}")
            except:
                print(f"Raw error: {response.text}")
    
    except Exception as e:
        print(f"\n✗ Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    print("File Upload Diagnostic Test\n")
    
    # Test resume upload
    test_resume_upload()
    
    # Test JD upload
    test_jd_upload()
    
    print("\n" + "=" * 80)
    print("Testing Complete")
    print("=" * 80)
