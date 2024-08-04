import os
import requests
from github import Github
from dotenv import load_dotenv
import openai
import git
import argparse

# Load environment variables
load_dotenv()

# GitHub and OpenAI API setup
github_token = os.getenv('GITHUB_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')
g = Github(github_token)

def get_github_repo_contents(repo_url):
    """Fetch all file contents from a GitHub repository."""
    repo_name = repo_url.split('/')[-2] + '/' + repo_url.split('/')[-1]
    repo = g.get_repo(repo_name)
    contents = repo.get_contents("")
    file_contents = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            try:
                file_contents.append((file_content.path, file_content.decoded_content.decode()))
            except:
                print(f"Could not decode {file_content.path}")
    return file_contents

def get_local_repo_contents(repo_path):
    """Fetch all file contents from a local Git repository."""
    repo = git.Repo(repo_path)
    file_contents = []
    for root, dirs, files in os.walk(repo_path):
        if '.git' in dirs:
            dirs.remove('.git')  # don't visit .git directories
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_path)
            if is_text_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    file_contents.append((relative_path, content))
                except UnicodeDecodeError:
                    print(f"Could not read {file_path}: Not a valid text file")
            else:
                print(f"Skipping non-text file: {file_path}")
    return file_contents

def combine_files(file_contents):
    """Combine all file contents into a single string."""
    combined = ""
    for path, content in file_contents:
        combined += f"File: {path}\n\n{content}\n\n"
    return combined



def is_text_file(file_path):
    """Check if a file is a text file."""
    text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.yml', '.yaml', '.toml', '.ini', '.cfg']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in text_extensions


def generate_readme(repo_content):
    """Generate README using OpenAI's GPT model."""
    prompt = f"""
    Based on the following repository content, generate a comprehensive README.md file. 
    Include sections such as project description, installation instructions, usage examples, and any other relevant information.
    Repository content:
    {repo_content[:4000]}  # Limiting to 4000 characters as an example
    Generate README:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Using a model with longer context
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates README files for GitHub repositories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    return response.choices[0].message['content']

def main():
    parser = argparse.ArgumentParser(description="Generate README for GitHub or local Git repository.")
    parser.add_argument("--local", help="Path to local Git repository")
    parser.add_argument("--github", help="URL of GitHub repository")
    args = parser.parse_args()

    if args.local:
        print(f"Processing local repository: {args.local}")
        file_contents = get_local_repo_contents(args.local)
    elif args.github:
        print(f"Processing GitHub repository: {args.github}")
        file_contents = get_github_repo_contents(args.github)
    else:
        repo_input = input("Enter the GitHub repository URL or local repository path: ")
        if os.path.isdir(repo_input):
            print(f"Processing local repository: {repo_input}")
            file_contents = get_local_repo_contents(repo_input)
        else:
            print(f"Processing GitHub repository: {repo_input}")
            file_contents = get_github_repo_contents(repo_input)

    combined_content = combine_files(file_contents)
    readme_content = generate_readme(combined_content)

    with open("README.md", "w") as f:
        f.write(readme_content)
    print("README.md has been generated successfully.")

if __name__ == "__main__":
    main()