#!/usr/bin/env python3

"""
AI VOICEOVER GENERATOR
Converts script to natural-sounding speech using gTTS (free) or ElevenLabs (premium)
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

VOICE_PROVIDER = os.getenv('VOICE_PROVIDER', 'gtts').lower()
OUTPUT_DIR = Path(__file__).parent / 'output'
VOICEOVER_PATH = OUTPUT_DIR / 'voiceover.mp3'

# Script from DEMO_VIDEO_GUIDE.md
SCRIPT = """
Tired of sending out dozens of resumes with no response? The problem might not be your experience. 
It's that your resume isn't optimized for Applicant Tracking Systems.

Introducing Resume2Interview. Our AI-powered platform analyzes your resume against any job description 
in seconds, giving you a detailed ATS compatibility score and specific recommendations to improve your chances.

Here's how it works. Simply upload your resume and paste the job description you're applying for. 
Our advanced AI analyzes both documents, comparing your skills, experience, and keywords against what 
the employer is looking for.

Within 60 seconds, you get a comprehensive ATS score showing exactly how well your resume matches. 
You'll see missing keywords that could boost your score, skills the employer wants that you should highlight, 
and specific sections of your resume that need improvement.

But we don't stop there. Resume2Interview provides actionable recommendations you can implement immediately. 
Add these missing keywords, highlight relevant experience, optimize your formatting for ATS systems.

The best part? It's completely free. No subscriptions, no hidden fees. Just instant, AI-powered resume optimization 
that helps you land more interviews.

Stop wondering why you're not getting callbacks. Start using Resume2Interview today and take control of your job search.

Visit resume2interview.com to try it now. Your next interview is just one optimized resume away.
"""

def generate_gtts_voiceover():
    """Generate voiceover using free Google Text-to-Speech"""
    try:
        from gtts import gTTS
        
        print("\n🎙️  Generating voiceover with gTTS (free)...\n")
        
        # Create TTS object
        tts = gTTS(text=SCRIPT, lang='en', slow=False)
        
        # Save to file
        tts.save(str(VOICEOVER_PATH))
        
        print(f"✅ Voiceover saved to: {VOICEOVER_PATH}")
        print("   Provider: Google Text-to-Speech (gTTS)")
        print("   Quality: Good (robotic but clear)")
        print("   Cost: FREE")
        
        return str(VOICEOVER_PATH)
        
    except ImportError:
        print("❌ Error: gTTS not installed")
        print("   Run: pip install gTTS")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating voiceover: {e}")
        sys.exit(1)

def generate_elevenlabs_voiceover():
    """Generate voiceover using premium ElevenLabs API"""
    try:
        import requests
        
        API_KEY = os.getenv('ELEVENLABS_API_KEY')
        if not API_KEY:
            print("❌ Error: ELEVENLABS_API_KEY not found in .env")
            print("   Get your API key from: https://elevenlabs.io/")
            sys.exit(1)
        
        print("\n🎙️  Generating voiceover with ElevenLabs (premium)...\n")
        
        # Voice ID for "Rachel" (default professional female voice)
        # You can change this to other voices from https://elevenlabs.io/docs/voices
        VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": API_KEY
        }
        
        data = {
            "text": SCRIPT,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        print("   Calling ElevenLabs API...")
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio file
            with open(VOICEOVER_PATH, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Voiceover saved to: {VOICEOVER_PATH}")
            print("   Provider: ElevenLabs")
            print("   Quality: Excellent (natural human-like)")
            print("   Cost: ~$0.30")
            
            return str(VOICEOVER_PATH)
        else:
            print(f"❌ ElevenLabs API error: {response.status_code}")
            print(f"   Response: {response.text}")
            print("\n💡 Falling back to free gTTS...")
            return generate_gtts_voiceover()
            
    except ImportError:
        print("❌ Error: requests library not installed")
        print("   Run: pip install requests")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating voiceover: {e}")
        print("\n💡 Falling back to free gTTS...")
        return generate_gtts_voiceover()

def get_audio_duration(audio_file):
    """Get duration of audio file in seconds"""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(audio_file)
        duration = len(audio) / 1000.0  # Convert milliseconds to seconds
        return duration
    except:
        # Fallback: estimate based on script length (avg 150 words/min)
        words = len(SCRIPT.split())
        estimated_duration = (words / 150) * 60
        return estimated_duration

def main():
    """Main entry point"""
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("AI VOICEOVER GENERATOR")
    print("=" * 60)
    
    # Generate voiceover based on provider
    if VOICE_PROVIDER == 'elevenlabs':
        voiceover_path = generate_elevenlabs_voiceover()
    else:
        voiceover_path = generate_gtts_voiceover()
    
    # Get duration
    try:
        duration = get_audio_duration(voiceover_path)
        print(f"   Duration: {duration:.1f} seconds")
    except:
        print("   Duration: ~90 seconds (estimated)")
    
    print("\n✅ Voiceover generation complete!\n")
    
    return voiceover_path

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
