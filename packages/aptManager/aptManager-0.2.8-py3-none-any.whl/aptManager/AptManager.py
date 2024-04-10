import subprocess
import json 

class AptManager(object):

    def __init__(self):
        self.connection = None
        self.cursor = None

    @staticmethod
    def add_gpg_key(link):
        try:
            command = f"wget -qO - {link} | apt-key add -"
            subprocess.run(command, shell=True)
            return None
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
            
    @staticmethod
    def upgrade_aurora():
        # Load JSON data from file 
        with open('/application-manager.json', 'r') as json_file:
            source = json.load(json_file)[0]
            
        # Generate aurora list 
        url = source["url"].rstrip('/')
        distribution = source["distribution"]
        components = source["components"]

        with open(f"/etc/apt/sources.list.d/aurora.list", "w") as aurora_list:
            aurora_list.write(f"deb {url} {distribution} {' '.join(components)}\n")

        # Generate environment
        APP_TO_INSTALL = source["packagesToInstall"]
        APP_TO_REMOVE = source["packagesToRemove"]

        with open('/etc/environment', 'w') as environment_file:
            environment_file.write(f"APP_TO_INSTALL={' '.join(APP_TO_INSTALL)}\n")
            environment_file.write(f"APP_TO_REMOVE={' '.join(APP_TO_REMOVE)}\n")
            
        # Start timer using systemctl
        process1 = subprocess.run(['systemctl', 'start', 'upgrade_aurora.timer'])
        print(process1.returncode)
        if process1.returncode == 0:
            print("Service has finished. Stopping the timer.")
            subprocess.run(['systemctl', 'stop', 'upgrade_aurora.timer'])


