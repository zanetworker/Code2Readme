# README.md

## Project Description

This project is a Python script designed to automatically generate a comprehensive `README.md` file for a GitHub repository or a local Git repository. By leveraging the GitHub API and OpenAI's language model, this tool fetches the contents of the project files and compiles a structured README that includes sections such as project description, installation instructions, usage examples, and more.

## Features

- Fetch contents of a GitHub repository directly using the GitHub API.
- Read and retrieve contents from a local Git repository.
- Supports various text file types including Python, JavaScript, Markdown, and HTML.
- Utilizes OpenAI's GPT model to generate a detailed README based on the gathered content.

## Installation Instructions

To get started with this project, follow the steps below:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/repository-name.git
   cd repository-name
   ```

2. **Install dependencies:**

   Make sure you have Python 3.x installed on your machine. You should also have Poetry installed for package management. If not, you can install it using pip:

   ```bash
   pip install poetry
   ```

   You can then install the required packages using Poetry:

   ```bash
   poetry install
   ```

   The `pyproject.toml` file should include the following packages:

   ```toml
   [tool.poetry.dependencies]
   python = "^3.8"
   requests = "*"
   PyGithub = "*"
   python-dotenv = "*"
   openai = "*"
   GitPython = "*"
   ```

3. **Set up environment variables:**

   This project requires GitHub and OpenAI API credentials. You can store these in a `.env` file in the root directory of the project:

   ```
   GITHUB_TOKEN=your_github_token
   OPENAI_API_KEY=your_openai_api_key
   ```

   Replace `your_github_token` and `your_openai_api_key` with your actual tokens.

## Usage Examples

To generate a README for a **local Git repository**, use the following command:

```bash
python main.py --local /path/to/your/local/repo
```

To generate a README for a **GitHub repository**, use this command:

```bash
python main.py --github https://github.com/username/repository-name
```

You can also run the script without any arguments, and it will prompt you to input either a local repository path or a GitHub repository URL:

```bash
python main.py
```

## How It Works

1. **Fetch Repository Contents:**
   - The script fetches file contents from either a specified GitHub repository or a local git repository.
  
2. **Combine File Contents:**
   - Text contents from the files are combined into a single string format.

3. **Generate README:**
   - A prompt containing the repository's file contents is sent to the OpenAI API to generate a structured README.

## Example Workflow

1. Run the script to process your desired repository (either local or GitHub).
2. The output will include a generated README that you can further customize or use directly in your repository.

## Contributing

Contributions are welcome! If you would like to improve this project, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please open an issue or contact the repository owner.

---

This README template provides all necessary information to get started with the project and understands its functionalities. Adjust any example paths or commands to suit your specific repository structure or usage patterns.