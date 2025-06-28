import subprocess

# Get list of all saved Wi-Fi profiles
try:
    data = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding='utf-8')
except subprocess.CalledProcessError:
    print("Error: Could not retrieve Wi-Fi profiles.")
    exit()

profiles = []
for line in data.splitlines():
    if "All User Profile" in line:
        parts = line.split(":")
        if len(parts) > 1:
            profiles.append(parts[1].strip())

# Display passwords of each profile
for profile in profiles:
    try:
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "profile", profile, "key=clear"],
            encoding='utf-8'
        )
        lines = result.splitlines()
        password = ""
        for line in lines:
            if "Key Content" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    password = parts[1].strip()
                    break
        print("{:<30}|  {:<}".format(profile, password))
    except subprocess.CalledProcessError:
        print("{:<30}|  {:<}".format(profile, "ACCESS DENIED or ERROR"))

