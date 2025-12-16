<div align="center">
  <img src="rezakora_banner.png" alt="ReZAKORA Banner" width="100%">

# 🤖 ReZAKORA-Bypass
  
  **The Next-Gen Audio reCAPTCHA Solver**
  
  [![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Patchright](https://img.shields.io/badge/Patchright-Undetected-7289da?style=for-the-badge)](https://github.com/Kaliiiiiiiiii/Patchright)
  [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
  [![Build Status](https://img.shields.io/badge/Build-Passing-success?style=for-the-badge)](https://github.com/DEEX404/ReZAKORA-Bypass/actions)

  <p align="center">
    <a href="#features">Features</a> •
    <a href="#installation">Installation</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#how-it-works">How It Works</a> •
    <a href="#disclaimer">Disclaimer</a>
  </p>
</div>

---

## ⚡ Overview

**"Are you a robot?" Yes. Yes I am.**

reCAPTCHA thinks it can stop us. It can't. **ReZAKORA-Bypass** leverages advanced audio transcription and the latest undetectable browser technology to solve challenges faster than a human ever could.

We use **Patchright** (undetected Playwright) to bypass bot detection triggers like `navigator.webdriver` and CDP fingerprinting, ensuring a high success rate on even the toughest sites.

## ✨ Features

| Feature | Description |
| :--- | :--- |
| **🛡️ Undetected** | Built on **Patchright**, completely bypassing modern bot detection systems. |
| **🚀 Fast & Efficient** | Intelligent polling (no fixed sleeps) and highly optimized logic for sub-second reaction times. |
| **🎙️ Google Speech AI** | Uses Google's own Speech Recognition API to transcribe audio challenges with high accuracy. |
| **🔄 Auto-Retry** | Robust error handling with automatic retry logic for network glitches or "Multiple solutions required" errors. |
| **📦 Clean API** | Single class design (`ReZAKORASolver`) that integrates easily into any Playwright script. |

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DEEX404/ReZAKORA-Bypass.git
cd ReZAKORA-Bypass
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Chromium & FFmpeg

**Chromium (Patchright):**

```bash
patchright install chromium
```

**FFmpeg (Required for audio conversion):**

- **Windows:** `choco install ffmpeg` or [Download Manual](https://ffmpeg.org/download.html)
- **Linux:** `sudo apt-get install ffmpeg`
- **Mac:** `brew install ffmpeg`

## 🚀 Quick Start

Get up and running in seconds. Here is a complete example:

```python
from patchright.sync_api import sync_playwright
from ReZakoraSolver import ReZAKORASolver

with sync_playwright() as p:
    # Launch browser (headless=False to see it in action)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to a page with reCAPTCHA
    page.goto("https://www.google.com/recaptcha/api2/demo")
    
    # Initialize and solve
    solver = ReZAKORASolver(page)
    solver.solveCaptcha()
    
    print("✅ Captcha successfully solved!")
    
    # Continue your automation...
    # page.click("#submit-button")
    
    browser.close()
```

## 🧪 Testing

Run the included test script to verify your setup against Google's demo page:

```bash
py test.py
```

It performs 3 automated solve attempts to ensure stability.

## 🧠 How It Works

1. **Detection**: Finds the reCAPTCHA iframes and handles.
2. **Interaction**: Clicks the checkbox simulating human behavior.
3. **Audio Bypass**: Switches to the audio challenge mode (easier for AI than images).
4. **Transcription**:
    - Downloads the audio challenge.
    - Converts format using `ffmpeg`.
    - Sends to **Google Speech API** for text transcription.
5. **Verification**: Submits the text and verifies the "solved" state using internal attributes (`aria-checked`).

## ⚠️ Disclaimer

> [!IMPORTANT]
> This tool is for **educational purposes only**.
>
> - Do not abuse this tool. Google may block your IP.
> - Always use proxies or VPNs when testing extensively.
> - Respect `robots.txt` and Terms of Service of target websites.

## 📄 License

This project is licensed under the **MIT License**.

---
