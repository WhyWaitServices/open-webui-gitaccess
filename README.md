# GitAccess
![GitAccess Logo](https://i.imgur.com/1PxbyHA.png)

**GitAccess** is a tool that enables LLM models to connect to a GitHub repository to fetch its contents. This way, you can query the model about the current state of the project and always stay up to date.

## 📦 Description
- **Author**: ErrorRExorY/CptExorY
- **Website**: [pascal-frerks.de](https://pascal-frerks.de)
- **GitHub Repo**: [GitAccess on GitHub](https://github.com/WhyWaitServices/open-webui-gitaccess.git)
- **Required OpenWebUI Version**: 0.6.0
- **Version**: 0.1.0
- **License**: MIT

## 🚀 Installation
To install GitAccess in your self-hosted OpenWebUI instance, you can follow these steps:

### Via the Marketplace
1. Open your OpenWebUI instance.
2. Go to the [Marketplace](https://openwebui.com/t/cptexory/gitaccess "Marketplace").
3. Add the link to GitAccess: `https://github.com/WhyWaitServices/open-webui-gitaccess.git`.

### Manual Installation
1. Copy the code from the `GitAccess.py` file.
2. Add the copied code to your OpenWebUI instance by creating a new tool under Workspace > Tools.
3. Paste the copied code from the `GitAccess.py` file into the large input field and assign a name and a description.
4. Save the tool.

## ⚙️ Configuration 
### Environment Variables (Valves)
- **Accessing the Valves**: The environment variables for the tool are set within OpenWebUI. Click the gear button when you open the tool to configure the valves.
  - **GITHUB_ACCESS_TOKEN**: A personal access token from GitHub that has the necessary permissions to access the repository.
  - **GITHUB_REPO_URL**: The URL of the GitHub repository, which should be specified in the format `username/repo`.

### UserValves
- **Setting UserValves**: If you have activated the tool in a chat or model, you can set the UserValves using the "Controls" button (located at the top right, directly left of the profile picture). A sheet will open where you can configure the UserValves of the tool.

## 🛠️ Usage
After installation, you can use GitAccess as follows:

1. Ensure that you are correctly configured (access token and repo URL).
2. Launch the tool in your OpenWebUI instance.
3. Use simple prompts like:
   - "What is the content of my GitHub repo?"
   - "Show me the content of two files in code blocks."

The response might look like this:
![Example Screenshot](https://i.imgur.com/tPMQwyf.png)

The status of actions will be displayed in the user interface through status messages.

## 🤖 Features
- **Fetching Repository Contents**: Read the structure and files of a specified GitHub repository.
- **Dynamic Filters**: Distinguish between directories and files to efficiently retrieve the desired data.
- **Event Emitter**: Real-time feedback on the progression of queries and other actions.

## 📋 License
This project is licensed under the MIT License. For more information, please refer to the [LICENSE](LICENSE) file.

## 🤝 Contributing
Contributions are welcome! Please open an issue or a pull request to share suggestions or propose improvements.

## 📞 Contact
For questions or feedback, you can contact me at [contact@example.com](mailto:contact@example.com).

Thank you for using GitAccess!