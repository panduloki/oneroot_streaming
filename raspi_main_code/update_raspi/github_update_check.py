import os
import subprocess
import requests

pexpect_installed = False
try:
    import pexpect
    pexpect_installed = True
except ImportError:
    print("pexpect module is not installed. You can install it using the command: pip install pexpect or pip3 install pexpect")

def check_internet():
    url = "http://www.google.com"
    timeout = 5
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def add_ssh_key_to_agent(ssh_key_path=None):
    
    if not os.path.exists(ssh_key_path):
        print(f"SSH key not found at {ssh_key_path}. Please generate an SSH key and add it to your GitHub account.")
        return
    try:
        passphrase = os.getenv("SSH_PASSPHRASE")
        if not passphrase:
            print("SSH_PASSPHRASE environment variable not set. Please set it using: export SSH_PASSPHRASE='your_passphrase'")
    except KeyError:
        print("KeyError: error getting passphrase from  environment variables. Please set it using: export SSH_PASSPHRASE='your_passphrase'")

    if os.path.exists(ssh_key_path):
        # Start the ssh-agent
        subprocess.run(["ssh-agent", "-s"], shell=True)
        # Add the SSH private key to the ssh-agent using pexpect to handle passphrase prompt
        child = pexpect.spawn(f"ssh-add {ssh_key_path}")
        if passphrase:
            child.expect("Enter passphrase for .*:")
            child.sendline(passphrase)
        child.interact()
    else:
        print(f"SSH key not found at {ssh_key_path}. Please generate an SSH key and add it to your GitHub account.")

def clone_repository(repo_url=None, repo_dir=None):
    if not repo_url:
        print("Please provide the repository URL.")
        return
    if not repo_dir and not os.path.exists(repo_dir):
        print("Please provide the repository directory.")
        return
    if not os.path.exists(repo_dir):
        print("Repository directory not found. please provide a valid directory.")
    else:
        print(f"clone the repository into the provided directory{repo_dir}")
        subprocess.run(["git", "clone", repo_url, repo_dir])
        # subprocess.run(["git", "-C", repo_dir, "pull"])

def pull_repository(repo_dir=None):
    if not os.path.exists(repo_dir):
        print(f"Repository directory {repo_dir} does not exist to update from git")
        return
    try:
        result = subprocess.run(["git", "-C", repo_dir, "pull", "origin", "main"], check=True, capture_output=True, text=True)
        print("git pull Output:", result.stdout)
        print("git pull Error:", result.stderr)
        print(f"Repository at {repo_dir} successfully updated.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull repository to rep_dir={repo_dir} error: {e}")
        print("Output:", e.stdout)
        print("Error:", e.stderr)



