#!/usr/bin/env python3

"""
VIDEO COMPILER
Combines screen recording with voiceover, adds text overlays and effects
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OUTPUT_DIR = Path(__file__).parent / 'output'
SCREEN_RECORDING = OUTPUT_DIR / 'screen-recording.webm'
VOICEOVER = OUTPUT_DIR / 'voiceover.mp3'
FINAL_VIDEO = OUTPUT_DIR / 'resume2interview-demo-final.mp4'

# Brand colors from config
BRAND_COLOR = "#2563EB"  # Blue
TEXT_COLOR = "white"

def compile_video():
    """Compile final video with all elements"""
    
    try:
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, TextClip, 
            CompositeVideoClip, concatenate_videoclips
        )
        from moviepy.video.fx.all import fadein, fadeout
        
        print("\n🎬 Compiling final video...\n")
        
        # Check input files exist
        if not SCREEN_RECORDING.exists():
            print(f"❌ Error: Screen recording not found at {SCREEN_RECORDING}")
            sys.exit(1)
        
        if not VOICEOVER.exists():
            print(f"❌ Error: Voiceover not found at {VOICEOVER}")
            sys.exit(1)
        
        # ============================================================
        # Load media files
        # ============================================================
        print("   Loading screen recording...")
        video = VideoFileClip(str(SCREEN_RECORDING))
        
        print("   Loading voiceover...")
        audio = AudioFileClip(str(VOICEOVER))
        
        # ============================================================
        # Adjust video duration to match audio
        # ============================================================
        audio_duration = audio.duration
        video_duration = video.duration
        
        print(f"   Video duration: {video_duration:.1f}s")
        print(f"   Audio duration: {audio_duration:.1f}s")
        
        if video_duration > audio_duration:
            # Speed up video slightly if it's longer than audio
            speedup_factor = video_duration / audio_duration
            if speedup_factor <= 1.2:  # Only if < 20% speedup needed
                video = video.fx(lambda clip: clip.speedx, speedup_factor)
                print(f"   Adjusted video speed: {speedup_factor:.2f}x")
            else:
                # Trim video to match audio
                video = video.subclip(0, audio_duration)
                print(f"   Trimmed video to: {audio_duration:.1f}s")
        elif audio_duration > video_duration:
            # Slow down video slightly if audio is longer
            slowdown_factor = video_duration / audio_duration
            if slowdown_factor >= 0.85:  # Only if < 15% slowdown needed
                video = video.fx(lambda clip: clip.speedx, slowdown_factor)
                print(f"   Adjusted video speed: {slowdown_factor:.2f}x")
            else:
                # Loop last frame to match audio duration
                extra_time = audio_duration - video_duration
                last_frame = video.to_ImageClip(video_duration - 0.1).set_duration(extra_time)
                video = concatenate_videoclips([video, last_frame])
                print(f"   Extended video with freeze frame: +{extra_time:.1f}s")
        
        # ============================================================
        # Replace video audio with voiceover
        # ============================================================
        print("   Replacing audio with voiceover...")
        video = video.set_audio(audio)
        
        # ============================================================
        # Add text overlays
        # ============================================================
        print("   Adding text overlays...")
        
        overlays = []
        
        # Overlay 1: "ATS Score: 78/100" (appears at ~30 seconds)
        try:
            ats_text = TextClip(
                "ATS Score: 78/100",
                fontsize=60,
                color='white',
                font='Arial-Bold',
                stroke_color=BRAND_COLOR,
                stroke_width=2
            ).set_position(('center', 150)).set_start(30).set_duration(5).crossfadein(0.5).crossfadeout(0.5)
            overlays.append(ats_text)
        except Exception as e:
            print(f"   ⚠ Warning: Could not create ATS text overlay: {e}")
        
        # Overlay 2: "15+ Missing Keywords" (appears at ~45 seconds)
        try:
            keywords_text = TextClip(
                "15+ Missing Keywords",
                fontsize=60,
                color='white',
                font='Arial-Bold',
                stroke_color=BRAND_COLOR,
                stroke_width=2
            ).set_position(('center', 150)).set_start(45).set_duration(5).crossfadein(0.5).crossfadeout(0.5)
            overlays.append(keywords_text)
        except Exception as e:
            print(f"   ⚠ Warning: Could not create keywords text overlay: {e}")
        
        # Overlay 3: "100% FREE" (appears at ~75 seconds)
        try:
            free_text = TextClip(
                "100% FREE",
                fontsize=70,
                color='#22C55E',  # Green
                font='Arial-Bold',
                stroke_color='white',
                stroke_width=3
            ).set_position(('center', 200)).set_start(75).set_duration(5).crossfadein(0.5).crossfadeout(0.5)
            overlays.append(free_text)
        except Exception as e:
            print(f"   ⚠ Warning: Could not create FREE text overlay: {e}")
        
        # Overlay 4: "resume2interview.com" (appears at ~85 seconds, stays until end)
        try:
            cta_text = TextClip(
                "resume2interview.com",
                fontsize=50,
                color='white',
                font='Arial-Bold',
                bg_color=BRAND_COLOR,
                method='caption',
                size=(None, None)
            ).set_position(('center', 900)).set_start(85).set_duration(video.duration - 85).crossfadein(0.5)
            overlays.append(cta_text)
        except Exception as e:
            print(f"   ⚠ Warning: Could not create CTA text overlay: {e}")
        
        # ============================================================
        # Composite video with overlays
        # ============================================================
        if overlays:
            print(f"   Compositing {len(overlays)} text overlays...")
            final_video = CompositeVideoClip([video] + overlays)
        else:
            print("   ⚠ No text overlays added (missing fonts or MoviePy issue)")
            final_video = video
        
        # ============================================================
        # Add fade in/out
        # ============================================================
        print("   Adding fade effects...")
        final_video = final_video.fx(fadein, 0.5).fx(fadeout, 1.0)
        
        # ============================================================
        # Export final video
        # ============================================================
        print(f"\n   Exporting final video to: {FINAL_VIDEO}")
        print("   This may take 5-10 minutes...\n")
        
        final_video.write_videofile(
            str(FINAL_VIDEO),
            codec='libx264',
            audio_codec='aac',
            fps=30,
            preset='medium',  # Balance between speed and quality
            threads=4,
            logger=None  # Suppress verbose output
        )
        
        # ============================================================
        # Cleanup
        # ============================================================
        video.close()
        audio.close()
        if overlays:
            for overlay in overlays:
                overlay.close()
        
        print(f"\n✅ Final video compiled!")
        print(f"   Output: {FINAL_VIDEO}")
        print(f"   Duration: {final_video.duration:.1f} seconds")
        print(f"   Resolution: {final_video.w}x{final_video.h}")
        
        final_video.close()
        
        return str(FINAL_VIDEO)
        
    except ImportError as e:
        print(f"❌ Error: Missing Python package: {e}")
        print("   Run: pip install moviepy")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error compiling video: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def generate_thumbnail():
    """Generate YouTube thumbnail from video"""
    try:
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        
        print("\n📸 Generating thumbnail...\n")
        
        if not FINAL_VIDEO.exists():
            print("   ⚠ Warning: Final video not found, skipping thumbnail")
            return None
        
        # Extract frame from middle of video
        video = VideoFileClip(str(FINAL_VIDEO))
        mid_time = video.duration / 2
        frame = video.get_frame(mid_time)
        video.close()
        
        # Convert to PIL Image
        img = Image.fromarray(frame)
        
        # Resize to YouTube thumbnail size (1280x720)
        img = img.resize((1280, 720), Image.Resampling.LANCZOS)
        
        # Apply slight blur to background
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Create drawing context
        draw = ImageDraw.Draw(img)
        
        # Add semi-transparent overlay at bottom
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([(0, 500), (1280, 720)], fill=(37, 99, 235, 200))  # Blue overlay
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        
        # Add text (simplified - use default PIL font)
        draw = ImageDraw.Draw(img)
        
        # Title text
        try:
            # Try to use a bold font if available
            font_large = ImageFont.truetype("arialbd.ttf", 80)
            font_medium = ImageFont.truetype("arial.ttf", 50)
        except:
            # Fallback to default
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        # Draw text with white color
        title_text = "Resume Optimizer"
        subtitle_text = "Get  More Interviews"
        
        # Center text
        draw.text((640, 550), title_text, fill='white', font=font_large, anchor='mm', stroke_width=3, stroke_fill='black')
        draw.text((640, 650), subtitle_text, fill='white', font=font_medium, anchor='mm', stroke_width=2, stroke_fill='black')
        
        # Save thumbnail
        thumbnail_path = OUTPUT_DIR / 'thumbnail.jpg'
        img.convert('RGB').save(thumbnail_path, 'JPEG', quality=95)
        
        print(f"✅ Thumbnail generated: {thumbnail_path}")
        
        return str(thumbnail_path)
        
    except Exception as e:
        print(f"   ⚠ Warning: Could not generate thumbnail: {e}")
        return None

def main():
    """Main entry point"""
    
    print("=" * 60)
    print("VIDEO COMPILER")
    print("=" * 60)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Compile video
    video_path = compile_video()
    
    # Generate thumbnail
    thumbnail_path = generate_thumbnail()
    
    print("\n✅ Video compilation complete!\n")
    
    return video_path, thumbnail_path

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
