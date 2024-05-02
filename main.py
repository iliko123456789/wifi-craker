import subprocess

def get_wifi_profiles():
    try:
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
        data = meta_data.decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [line.split(":")[1][1:-1] for line in data if "All User Profile" in line]
        return profiles
    except subprocess.CalledProcessError as e:
        print("Error occurred while fetching Wi-Fi profiles:", e)
        return []

def get_wifi_password(profile):
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
        results = results.decode('utf-8', errors="backslashreplace").split('\n')
        password_lines = [line.split(":")[1][1:-1] for line in results if "Key Content" in line]
        if password_lines:
            password = password_lines[0]
        else:
            password = "Password not found"
        return password
    except subprocess.CalledProcessError as e:
        return f"Error retrieving password for {profile}: {e}"

def main():
    print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
    print("-" * 46)
    profiles = get_wifi_profiles()
    for profile in profiles:
        password = get_wifi_password(profile)
        print("{:<30}| {:<}".format(profile, password))

if __name__ == "__main__":
    main()
