# updater.py - Checks for new version and updates BeeLogger using git
# Compatible with Python 3.x

import subprocess  # For running shell commands
import urllib.request  # For downloading files from the internet


# Compares the local version with the remote version
# Returns True if an update is needed, False otherwise
def update_client_version(version):
    with open("version.txt", "r") as vnum:
        local_version = vnum.read().strip()  # Read the local version from file
        remote_version = version.strip()     # Clean up the remote version string
        if local_version != remote_version:
            return True  # Update needed
        else:
            return False  # No update needed

# Main update logic
# Downloads the latest version number from GitHub
# If the local version is outdated, pulls the latest code from git
def main():
    url = "https://raw.githubusercontent.com/4w4k3/BeeLogger/master/version.txt"  # URL to the remote version file
    # Download the remote version number
    with urllib.request.urlopen(url) as response:
        version = response.read().decode('utf-8').strip()  # Read and decode the remote version
    # Compare local and remote versions
    if update_client_version(version):
        # If update needed, pull latest code from git
        subprocess.call(["git", "pull", "origin", "master"])
        return "[*] Updated to latest version: v{}..".format(version)
    else:
        # If already up to date, notify user
        return "[*] You are already up to date with git origin master."



# Check for updates and prints the result
if __name__ == '__main__':
    print("[*] Checking version information..")
    # Calling the main function to check for updates
    print(main())
