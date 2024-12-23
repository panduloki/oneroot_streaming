from subprocess_command import run_command

def check_main_system_updates():
    commands = [
        ['sudo', 'apt-get', 'update'],
        ['sudo', 'apt-get', 'upgrade', '-y'],
        ['sudo', 'apt-get', 'dist-upgrade', '-y'],
        ['sudo', 'apt', 'update'],
        ['sudo', 'apt', 'full-upgrade', '-y'],
        ['sudo', 'apt-get', 'autoremove', '-y'],
        ['sudo', 'apt-get', 'clean']
    ]
    
    for command in commands:
        run_command(command)
    #TODO put logging
    print("System update and cleanup completed successfully.")

