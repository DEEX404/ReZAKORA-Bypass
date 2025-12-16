"""
ReZAKORA-Bypass - Fast reCAPTCHA Solver
Uses Patchright (undetected Playwright) + Google Speech API
"""

import os
import urllib.request
import random
import pydub
import speech_recognition
from patchright.sync_api import sync_playwright, TimeoutError, expect


class ReZAKORASolver:
    """Fast reCAPTCHA solver using Patchright (undetected Playwright) + Google Speech."""
    
    TEMP_DIR = os.getenv("TEMP") if os.name == "nt" else "/tmp"
    
    def __init__(self, page, timeout: int = 15000, max_retries: int = 3) -> None:
        self.page = page
        self.timeout = timeout
        self.max_retries = max_retries

    def solve(self) -> bool:
        """Solve the reCAPTCHA with automatic retries."""
        for attempt in range(self.max_retries):
            try:
                return self._solve()
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise
                self.page.wait_for_timeout(500)  # Reduced retry wait
        return False

    def _solve(self) -> bool:
        """Core solving logic."""
        
        # 1. Click checkbox
        checkbox_frame = self.page.frame_locator("iframe[title='reCAPTCHA']")
        checkbox = checkbox_frame.locator(".recaptcha-checkbox-border")
        checkbox.wait_for(state="visible", timeout=self.timeout)
        checkbox.click()
        
        # 2. Check if solved immediately
        # Fast check without explicit wait
        if self._is_solved():
            return True
        
        # 3. Wait for challenge and click audio
        # Optimistic wait - don't wait for frame wrapper if not needed
        challenge_frame = self.page.frame_locator("iframe[title*='recaptcha challenge']")
        audio_btn = challenge_frame.locator("#recaptcha-audio-button")
        audio_btn.wait_for(state="visible", timeout=self.timeout)
        audio_btn.click()
        
        # 4. Check for bot detection (fast check)
        if self._is_detected(challenge_frame):
            raise Exception("Bot detected")
        
        # 5. Solve audio challenges
        max_audio_attempts = 5
        for audio_attempt in range(max_audio_attempts):
            # Wait for audio source
            audio_source = challenge_frame.locator("#audio-source")
            audio_source.wait_for(state="attached", timeout=self.timeout)
            
            # Smart wait for src attribute
            audio_url = None
            for _ in range(100): # 5 seconds max (50ms * 100)
                audio_url = audio_source.get_attribute("src")
                if audio_url:
                    break
                self.page.wait_for_timeout(50) 
                
            if not audio_url:
                raise Exception("Audio source not found")
                
            answer = self._transcribe(audio_url)
            print(f"Transcribed: {answer}")
            
            # Submit answer
            audio_input = challenge_frame.locator("#audio-response")
            audio_input.fill(answer.lower())
            challenge_frame.locator("#recaptcha-verify-button").click()
            
            # Fast verification check loop
            # Race condition: Success OR Error OR Detection
            for _ in range(40): # 2 seconds max check (50ms interval)
                self.page.wait_for_timeout(50)
                
                if self._is_solved():
                    return True
                
                # Check errors using JS for speed
                # usage: locator("body").evaluate(js) runs js in the frame
                status = challenge_frame.locator("body").evaluate(CHECK_STATUS_JS)
                if status == 'multiple':
                    print(f"Multiple solutions required... ({audio_attempt + 1}/{max_audio_attempts})")
                    break # Break inner loop to retry audio
                elif status == 'detected':
                    raise Exception("Bot detected")
            
            # If we broke efficiently or timed out checking solved, loop continues to next audio attempt
            if self._is_solved():
                return True
        
        raise Exception("Failed after multiple audio attempts")

    def _is_solved(self) -> bool:
        """Check if captcha is solved (fast)."""
        try:
            checkbox_frame = self.page.frame_locator("iframe[title='reCAPTCHA']")
            
            # 1. Check for the checked class on the span (most reliable)
            if checkbox_frame.locator(".recaptcha-checkbox-checked").count() > 0:
                return True
                
            # 2. Check aria-checked attribute
            checkbox = checkbox_frame.locator(".recaptcha-checkbox")
            if checkbox.get_attribute("aria-checked") == "true":
                return True
                
            # 3. Backup check using style on checkmark
            style = checkbox_frame.locator(".recaptcha-checkbox-checkmark").get_attribute("style")
            return style and len(style) > 0
        except:
            return False

    def _is_detected(self, challenge_frame) -> bool:
        """Check if bot was detected."""
        try:
            return challenge_frame.locator("text=Try again later").is_visible(timeout=500)
        except:
            return False

    def _transcribe(self, audio_url: str) -> str:
        """Download and transcribe audio using Google Speech API."""
        mp3 = os.path.join(self.TEMP_DIR, f"rz_{random.randint(1000,9999)}.mp3")
        wav = os.path.join(self.TEMP_DIR, f"rz_{random.randint(1000,9999)}.wav")
        
        try:
            urllib.request.urlretrieve(audio_url, mp3)
            pydub.AudioSegment.from_mp3(mp3).export(wav, format="wav")
            
            recognizer = speech_recognition.Recognizer()
            with speech_recognition.AudioFile(wav) as src:
                audio = recognizer.record(src)
            
            return recognizer.recognize_google(audio)
        finally:
            for f in (mp3, wav):
                try: os.remove(f)
                except: pass


# Backward compatibility alias
RecaptchaSolver = ReZAKORASolver

# Helper for wait_for_function (injected script)
CHECK_STATUS_JS = """
() => {
    // Check if solved (checkbox frame) - handled in python because cross-frame
    // Check error/detection (challenge frame)
    const error = document.querySelector('.rc-audiochallenge-error-message');
    if (error) {
        const text = error.innerText || "";
        if (text.includes('Multiple') || text.includes('multiple') || text.includes('solve more')) {
            return 'multiple';
        }
    }
    
    if (document.body.innerText.includes('Try again later')) {
        return 'detected';
    }
    
    return false;
}
"""
