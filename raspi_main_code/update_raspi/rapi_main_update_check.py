from github_update_check import add_ssh_key_with_passphrase, pull_repository_using_subprocess , check_internet, check_git_status_using_subprocess
from system_update_check import check_main_system_updates
from tailscale_update_check import check_tailscale_status

if __name__ == "__main__":
    repo_url = "git@github.com:panduloki/oneroot_streaming.git"
    repo_dir = "/home/oneroot/Desktop/oneroot_streaming/"
    ssh_key_path1 = "/home/oneroot/Desktop/ssh_key/id1"
    if check_internet():
        #check_main_system_updates()
        
        #add_ssh_key_with_passphrase(ssh_key_path= ssh_key_path1, passphrase= "oneroot")

        #check_git_status_using_subprocess(repo_dir)
        
        #pull_repository_using_subprocess(repo_dir)

        #check_tailscale_status()

        

    else:
        print("No internet connection. Please check your connection and try again.")
