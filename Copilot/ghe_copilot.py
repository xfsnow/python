# use Python to call GitHub Copilot API
# create a user based on SAML SSO
# Enable the user GitHub Copilot usage
# Reference doc: 
# https://docs.github.com/en/github-ae@latest/rest/reference/enterprise-admin#create-a-user
# https://docs.github.com/en/github-ae@latest/rest/reference/enterprise-admin#enable-github-copilot-for-a-user

# Usage: python ghe_copilot.py <token> <username> <email>

import requests
import json
import sys

# Create a user based on SAML SSO
def create_user(token, username, email):
    url = "https://api.github.com/admin/users"
    payload = json.dumps({
        "login": username,
        "email": email,
        "name": username,
        "active": True,
        "private": False,
        "restricted": False,
        "allow_squash_merge": True,
        "allow_merge_commit": True,
        "allow_rebase_merge": True,
        "allow_auto_merge": False,
        "two_factor_requirement_enabled": False,
        "user_type": "user",
        "owned_private_repos": 0,
        "plan": {
            "name": "free",
            "private_repos": 0,
            "space": 976562499,
            "collaborators": 0
        }
    })
    headers = {
        'Authorization': 'token ' + token,
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 201:
        print("User created successfully!")
    else:
        print("User created failed!")
        print(response.text.encode('utf8'))

# Enable the user GitHub Copilot usage
def enable_copilot(token, username):
    url = "https://api.github.com/users/" + username + "/interaction-limits"
    payload = json.dumps({
        "limit": "unlimited",
        "origin": "cli"
    })
    headers = {
        'Authorization': 'token ' + token,
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.sombra-preview+json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    if response.status_code == 200:
        print("User GitHub Copilot enabled successfully!")
    else:
        print("User GitHub Copilot enabled failed!")
        print(response.text.encode('utf8'))

# Main function
def main():
    # check input parameters
    if len(sys.argv) != 4:
        print("Usage: python ghe_copilot.py <token> <username> <email>")
        sys.exit(1)
    # Get the token from the command line
    token = sys.argv[1]
    # Get the username from the command line
    username = sys.argv[2]
    # Get the email from the command line
    email = sys.argv[3]
    # Create a user based on SAML SSO
    create_user(token, username, email)
    # Enable the user GitHub Copilot usage
    enable_copilot(token, username)

if __name__ == "__main__":
    main()

