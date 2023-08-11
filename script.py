import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
input_file_path = 'data/input.csv'
output_file_path = 'data/output.csv'
user_data_dict = {}

with open(input_file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    rows = list(csv_reader)

def fetch_github_user_data(username):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()

for row in rows:
    username = row['Username']
    if username and username not in user_data_dict:
        print(f"Processing: {username}")
        github_data = fetch_github_user_data(username)
        
        name = github_data.get('name', '')
        email = github_data.get('email', '')
        blog = github_data.get('blog', '')
        twitter = github_data.get('twitter_username', '')
        location = github_data.get('location', '')
        company = github_data.get('company', '')
        followers = github_data.get('followers', '')
        
        user_data = [username, name, email, blog, twitter, location, company, followers]
        user_data_dict[username] = user_data

with open(output_file_path, 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Username', 'Name', 'Email', 'Blog', 'Twitter', 'Location', 'Company', 'Followers'])
    csv_writer.writerows(user_data_dict.values())

print("Data written to", output_file_path)
