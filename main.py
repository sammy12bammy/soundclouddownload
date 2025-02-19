import os
import sys
import subprocess
import platform

def get_desktop_path():
    """Get the desktop path for different operating systems."""
    return os.path.join(os.path.expanduser("~"), "Desktop")

def create_songs_folder():
    """Create a 'songs' folder on the desktop."""
    desktop_path = get_desktop_path()
    songs_folder = os.path.join(desktop_path, "songs")
    os.makedirs(songs_folder, exist_ok=True)  # Create folder if it doesn’t exist
    return songs_folder

def is_installed(command):
    """Check if a command exists on the system."""
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_pip():
    """Install pip if missing."""
    print("pip is not installed. Installing pip...")
    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)

def install_scdl():
    """Install scdl using pip."""
    print("Installing scdl...")
    subprocess.run([sys.executable, "-m", "pip", "install", "scdl"], check=True)

def install_ffmpeg():
    """Install ffmpeg based on the OS."""
    print("Installing ffmpeg...")
    system = platform.system()
    
    if system == "Windows":
        print("Please install FFmpeg manually from https://ffmpeg.org/download.html and add it to PATH.")
    elif system == "Darwin":  # macOS
        if not is_installed("brew"):
            print("Installing Homebrew first...")
            subprocess.run(
                ["/bin/bash", "-c", 
                 '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'], 
                check=True
            )
        subprocess.run(["brew", "install", "ffmpeg"], check=True)
    elif system == "Linux":
        subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)

def convert_to_high_quality_mp3(directory):
    """Convert all non-MP3 files in the directory to 320kbps MP3 using ffmpeg."""
    for filename in os.listdir(directory):
        if filename.endswith(".m4a") or filename.endswith(".ogg") or filename.endswith(".wav"):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, os.path.splitext(filename)[0] + ".mp3")

            print(f"Converting {filename} to 320kbps MP3...")
            subprocess.run(["ffmpeg", "-i", input_path, "-b:a", "320k", output_path], check=True)

            # Optional: Delete the original non-MP3 file after conversion
            os.remove(input_path)

# Step 1: Ensure pip is installed
print("Checking pip")
if not is_installed("pip"):
    install_pip()

# Step 2: Check and install scdl and ffmpeg
print("Checking scdl and ffmpeg")
if not is_installed("scdl"):
    install_scdl()

if not is_installed("ffmpeg"):
    install_ffmpeg()

# Step 3: Create the "songs" folder on the Desktop
songs_folder = create_songs_folder()

# Step 4: Download a SoundCloud song
soundcloud_url = input("Enter SoundCloud song or playlist URL: ")

command = f"scdl -l {soundcloud_url} -o \"{songs_folder}\" --path-template \"%(title)s.%(ext)s\" --onlymp3"
os.system(command)

# Step 5: Convert to high-quality 320kbps MP3 if needed
convert_to_high_quality_mp3(songs_folder)

print(f"Download complete! Check the '{songs_folder}' folder on your Desktop.")

