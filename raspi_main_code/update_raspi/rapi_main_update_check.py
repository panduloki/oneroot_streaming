from github_update_check import add_ssh_key_to_agent, pull_repository , check_internet

if __name__ == "__main__":
    repo_url = "git@github.com:panduloki/oneroot_streaming.git"
    repo_dir = "/home/oneroot/Desktop/oneroot_streaming/"
    ssh_key_path1 = "/home/oneroot/Desktop/ssh_key/id1"
    if check_internet():
        add_ssh_key_to_agent(ssh_key_path= ssh_key_path1)
        #update_repository()
        pull_repository(repo_dir)
    else:
        print("No internet connection. Please check your connection and try again.")
