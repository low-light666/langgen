import json

# Load your JSON data
with open('francais.json', 'r') as file:
    json_data = json.load(file)


# Initialize README content
readme_content = "# Machine generate French Grammar playlist\n\n"

# Iterate through the levels and topics to create the README content
for level, topics in json_data.items():
    readme_content += f"## Level {level}\n\n"
    for num, details in topics.items():
        readme_content += f"### {details['topic']}\n"
        readme_content += f"- Query: `{details['query']}`\n"
        readme_content += f"- Link: [{details['link']}]({details['link']})\n\n"

# Write the README content to a file
with open('README.md', 'w', encoding='utf-8') as readme_file:
    readme_file.write(readme_content)

print("README.md file created successfully!")
