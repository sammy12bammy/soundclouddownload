import os
import sys
import subprocess
import platform

def is_installed(command):
    """Check if a command exists on the system"""
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_pip():
    """Install pip if missing"""
    print("pip is not installed. Installing pip...")
    try:
        # Download and install pip
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    except Exception as e:
        print("Error installing pip:", e)
        sys.exit(1)

def install_scdl():
    """Install scdl using pip"""
    print("Installing scdl...")
    subprocess.run([sys.executable, "-m", "pip", "install", "scdl"], check=True)

def install_homebrew():
    """Install Homebrew on macOS if not installed"""
    print("Homebrew is not installed. Installing Homebrew...")
    subprocess.run(
        ["/bin/bash", "-c", 
         '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'], 
        check=True
    )

def install_ffmpeg():
    """Install ffmpeg based on the OS"""
    print("Installing ffmpeg...")
    system = platform.system()
    
    if system == "Windows":
        print("Please install FFmpeg manually from https://ffmpeg.org/download.html and add it to PATH.")
    elif system == "Darwin":  # macOS
        if not is_installed("brew"):
            install_homebrew()
        subprocess.run(["brew", "install", "ffmpeg"], check=True)
    elif system == "Linux":
        subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)

# Step 1: Ensure pip is installed
if not is_installed("pip"):
    install_pip()

# Step 2: Check and install scdl and ffmpeg
if not is_installed("scdl"):
    install_scdl()

if not is_installed("ffmpeg"):
    install_ffmpeg()

# Step 3: Download a SoundCloud song
soundcloud_url = "https://soundcloud.com/user-643905711/over-critical-1?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing"

# Output directory
output_dir = "./downloads"
os.makedirs(output_dir, exist_ok=True)

# Download command
command = f"scdl -l {soundcloud_url} -o {output_dir} --path-template \"%(title)s.%(ext)s\""
os.system(command)

print(f"Download complete! Check the '{output_dir}' folder.")
