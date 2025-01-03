import os
import sys
import requests
import subprocess
from subprocess_command import run_command  # Import the run_command function from subprocess_command.py

# Check if GitPython is installed
try:
    import git

    def clone_repository_using_gitpython(repo_url, repo_dir):
        if not os.path.exists(repo_dir):
            try:
                print(f"Cloning repository from {repo_url} to {repo_dir}...")
                git.Repo.clone_from(repo_url, repo_dir)
                print(f"Repository successfully cloned to {repo_dir}.")
            except git.exc.GitCommandError as e:
                print(f"Failed to clone repository from {repo_url} to {repo_dir}. Error: {e}")
        else:
            print(f"Repository directory {repo_dir} already exists.")

    def pull_repository_using_gitpython(repo_dir):
        if not os.path.exists(repo_dir):
            print(f"Repository directory {repo_dir} does not exist to update from git.")
            return
        try:
            repo = git.Repo(repo_dir)
            origin = repo.remotes.origin
            origin.pull('main')
            print(f"Repository at {repo_dir} successfully updated.")
        except git.exc.GitCommandError as e:
            print(f"Failed to pull repository to repo_dir={repo_dir}. Error: {e}")
except ImportError:
    print("GitPython is not installed. Please install it using 'pip install gitpython'.")
    #sys.exit(1)

def check_internet():
    url = "http://www.google.com"
    timeout = 5
    try:
        print("Checking internet...")
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print("Internet connection is active.")
            return True
        else:
            print(f"Received unexpected status code after checking with google {response.status_code}")
            return False
    except (requests.ConnectionError, requests.Timeout) as e:
        print(f"Error while checking internet connection: {e}")
        return False

def add_ssh_key_with_passphrase(ssh_key_path, passphrase):
    """Add the SSH key to ssh-agent using subprocess to handle the passphrase prompt."""
    
    print("\n<----------- adding ssh key with passphrase ----------------->")
    if not os.path.exists(ssh_key_path):
        print(f"SSH key not found at {ssh_key_path}.")
        #sys.exit(1)

    try:
        print("Adding SSH key to ssh-agent with passphrase handling...")

        # Start the ssh-add process
        process = subprocess.Popen(
            ["ssh-add", ssh_key_path],
            stdin=subprocess.PIPE,  # Open stdin to pass the passphrase
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send the passphrase to stdin
        stdout, stderr = process.communicate(input=f"{passphrase}\n")

        if process.returncode == 0:
            print("SSH key added successfully.")
            print("stdout output  after running ssh-add command:", stdout)
        else:
            print("Failed to add SSH key:")
            print("stdout error after running ssh-add command:", stderr)
        
        # Print stdout if it asks for passphrase
        if "Enter passphrase for" in stdout:
            print(stdout)
            process.communicate(input=f"{passphrase}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

def clone_repository_using_subprocess(repo_url=None, repo_dir=None):
    if not repo_url:
        print("Please provide the repository URL.")
        return
    if not repo_dir:
        print("Please provide the repository directory.")
        return
    if os.path.exists(repo_dir):
        print("Repository directory already exists. Please provide a different directory or delete the existing one.")
        return

    print(f"Cloning the repository into the directory: {repo_dir}")
    run_command(["git", "clone", repo_url, repo_dir])

def pull_repository_using_subprocess(repo_dir=None):
    if not os.path.exists(repo_dir):
        print(f"Repository directory {repo_dir} does not exist to update from git.")
        return
    
    result = run_command(["git", "-C", repo_dir, "pull", "origin", "main"])
    if result.returncode != 0:
        print(f"Failed to update repository at {repo_dir}. Error: {result.stderr}")
    else:
        print(f"Repository at {repo_dir} successfully updated.")
    
"""TODO if these lines are in output
    Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
  modified:   raspi_main_code/update_raspi/github_update_check.py
  no changes added to commit (use "git add" and/or "git commit -a")
  
  using sting manipulation print you need to commit changes or pull again for changes if not updated
"""

def check_git_status_using_subprocess(repo_dir=None):
    if not os.path.exists(repo_dir):
        print(f"Repository directory {repo_dir} does not exist to check status.")
        return
    
    run_command(["git", "-C", repo_dir, "status"])
       

# # Check internet connectivity
# if check_internet():
#     print("Internet connection is active.")
# else:
#     print("No internet connection detected.")

