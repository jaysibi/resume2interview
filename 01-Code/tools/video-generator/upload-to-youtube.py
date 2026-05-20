#!/usr/bin/env python3

"""
YOUTUBE UPLOADER
Uploads video to YouTube with optimized metadata using YouTube Data API v3
"""

import os
import sys
import json
import pickle
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OUTPUT_DIR = Path(__file__).parent / 'output'
VIDEO_FILE = OUTPUT_DIR / 'resume2interview-demo-final.mp4'
THUMBNAIL_FILE = OUTPUT_DIR / 'thumbnail.jpg'
CREDENTIALS_FILE = Path(__file__).parent / 'youtube_credentials.json'
TOKEN_FILE = Path(__file__).parent / 'token.pickle'

# YouTube metadata from YOUTUBE_UPLOAD_INSTRUCTIONS.md
TITLE = "Resume Optimizer AI - Get More Interviews with ATS-Optimized Resumes"

DESCRIPTION = """Tired of applying to jobs and hearing nothing back? Your resume might not be optimized for Applicant Tracking Systems (ATS).

Resume2Interview uses AI to analyze your resume against any job description in seconds, giving you a detailed ATS score and actionable recommendations to improve your chances of landing interviews.

⏱️ TIMESTAMPS:
0:00 - The Problem: Why ATS Matters
0:15 - Introducing Resume2Interview
0:25 - How It Works
0:35 - Upload Your Resume
0:45 - Get Your ATS Score
0:55 - Actionable Recommendations
1:10 - 100% Free Forever
1:20 - Try It Now

✨ KEY FEATURES:
• Instant ATS compatibility analysis
• Detailed keyword matching
• Missing skills identification
• Formatting optimization tips
• 100% free - no subscriptions, no hidden fees
• Works with any job description
• Get results in under 60 seconds

🎯 PERFECT FOR:
• Job seekers who aren't getting interview callbacks
• Career changers optimizing resumes for new industries
• Recent graduates entering the job market
• Professionals applying to competitive positions
• Anyone wanting to improve their resume's ATS score

💡 HOW TO USE:
1. Visit resume2interview.com
2. Upload your resume (PDF, DOC, or TXT)
3. Paste the job description
4. Get instant analysis and recommendations
5. Update your resume with suggested improvements

🚀 START LANDING MORE INTERVIEWS TODAY:
👉 https://resume2interview.com

#ResumeOptimization #ATSResume #JobSearch #CareerAdvice #ResumeTips #InterviewTips #JobHunting #CareerGrowth #ATS #ResumeHelp"""

TAGS = [
    "resume optimization",
    "ATS resume",
    "job search tips",
    "resume tips",
    "career advice",
    "interview tips",
    "applicant tracking system",
    "resume keywords",
    "job application tips",
    "career growth",
    "resume analyzer",
    "AI resume",
    "resume scanner",
    "job hunting",
    "resume help",
    "career coach",
    "job search strategy",
    "resume writing",
    "get more interviews",
    "resume improvement",
    "free resume tools",
    "resume checker",
    "ATS optimization",
    "job search 2024",
    "resume2interview"
]

CATEGORY_ID = "27"  # Education category
PRIVACY_STATUS = "public"  # Can be: public, unlisted, private

def authenticate_youtube():
    """Authenticate with YouTube API using OAuth 2.0"""
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        # Scopes required for video upload
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        creds = None
        
        # Check if we have saved credentials
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("   Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    print(f"❌ Error: YouTube credentials file not found: {CREDENTIALS_FILE}")
                    print("\n   📝 To get credentials:")
                    print("   1. Go to: https://console.cloud.google.com/")
                    print("   2. Create a project (or select existing)")
                    print("   3. Enable YouTube Data API v3")
                    print("   4. Create OAuth 2.0 credentials (Desktop app)")
                    print("   5. Download as 'youtube_credentials.json'")
                    print(f"   6. Place in: {CREDENTIALS_FILE.parent}\n")
                    sys.exit(1)
                
                print("\n🔐 First time setup: Opening browser for authentication...")
                print("   Please authorize the application when prompted.\n")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES
                )
                creds = flow.run_local_server(port=0)
                
                # Save credentials for future runs
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                
                print("✅ Authentication successful! Credentials saved.\n")
        
        # Build YouTube API client
        youtube = build('youtube', 'v3', credentials=creds)
        
        return youtube
        
    except ImportError as e:
        print(f"❌ Error: Missing Python package: {e}")
        print("   Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def upload_video(youtube):
    """Upload video to YouTube"""
    
    try:
        from googleapiclient.http import MediaFileUpload
        
        print(f"📤 Uploading video to YouTube...\n")
        
        # Check video file exists
        if not VIDEO_FILE.exists():
            print(f"❌ Error: Video file not found: {VIDEO_FILE}")
            sys.exit(1)
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': TITLE,
                'description': DESCRIPTION,
                'tags': TAGS,
                'categoryId': CATEGORY_ID
            },
            'status': {
                'privacyStatus': PRIVACY_STATUS,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create MediaFileUpload object
        media = MediaFileUpload(
            str(VIDEO_FILE),
            mimetype='video/mp4',
            resumable=True,
            chunksize=1024*1024  # 1MB chunks
        )
        
        # Execute upload request
        print(f"   Title: {TITLE[:60]}...")
        print(f"   File: {VIDEO_FILE.name}")
        print(f"   Size: {VIDEO_FILE.stat().st_size / (1024*1024):.1f} MB")
        print(f"   Privacy: {PRIVACY_STATUS}")
        print("\n   Uploading (this may take 5-10 minutes)...\n")
        
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"   Upload progress: {progress}%", end='\r')
        
        print("\n")
        
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        print(f"✅ Video uploaded successfully!")
        print(f"   Video ID: {video_id}")
        print(f"   URL: {video_url}")
        
        # Save video ID for later use
        video_id_file = OUTPUT_DIR / 'video-id.txt'
        with open(video_id_file, 'w') as f:
            f.write(video_id)
        
        # Upload thumbnail if available
        if THUMBNAIL_FILE.exists():
            upload_thumbnail(youtube, video_id)
        
        # Write detailed log
        log_file = OUTPUT_DIR / 'youtube-upload-log.txt'
        with open(log_file, 'w') as f:
            f.write(f"YouTube Upload Log\n")
            f.write(f"==================\n\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {video_url}\n")
            f.write(f"Title: {TITLE}\n")
            f.write(f"Privacy: {PRIVACY_STATUS}\n")
            f.write(f"Category: {CATEGORY_ID}\n")
            f.write(f"\nMetadata saved to: {video_id_file}\n")
        
        return video_id, video_url
        
    except Exception as e:
        print(f"❌ Upload error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def upload_thumbnail(youtube, video_id):
    """Upload custom thumbnail to video"""
    
    try:
        from googleapiclient.http import MediaFileUpload
        
        print(f"\n📸 Uploading thumbnail...\n")
        
        media = MediaFileUpload(str(THUMBNAIL_FILE), mimetype='image/jpeg')
        
        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=media
        )
        
        response = request.execute()
        
        print(f"✅ Thumbnail uploaded!")
        
    except Exception as e:
        print(f"   ⚠ Warning: Could not upload thumbnail: {e}")
        print("   You can upload manually in YouTube Studio")

def main():
    """Main entry point"""
    
    print("=" * 60)
    print("YOUTUBE UPLOADER")
    print("=" * 60)
    print()
    
    # Authenticate
    youtube = authenticate_youtube()
    
    # Upload video
    video_id, video_url = upload_video(youtube)
    
    print("\n✅ YouTube upload complete!\n")
    print(f"🎥 Watch your video: {video_url}")
    print(f"📊 Analytics: https://studio.youtube.com\n")
    
    return video_id, video_url

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)
