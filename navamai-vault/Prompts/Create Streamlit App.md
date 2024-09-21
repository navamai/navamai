## Create Streamlit App

Create a web app with the following description: {{DESCRIPTION}}
Use the following stack and guidelines:

Framework: Streamlit
Styling: Native Streamlit components + Custom CSS (if needed)
Data visualization: Plotly, Matplotlib, or Altair
Data storage: Local file system or SQLite database
Additional libraries: Include via pip as needed
Language: Python

Provide key code snippets for the main functionality, including:
1. app.py as the main script
2. Any crucial custom functions or classes
3. State management setup (using Streamlit session state)
4. Data loading and processing implementation

Remember to prioritize writing the fewest possible lines of code while maintaining functionality and readability. Utilize Streamlit's built-in components and functions where appropriate to minimize custom code.
Ensure all functionality runs locally without requiring any cloud services.

Generate code for the entire app as a markdown formatted response with separate code blocks for each file. Each code block should be preceded with a level 2 heading - File: file-name.ext. 

Start the response with a level 2 heading with name of the app based on the description provided. Add the description as provided below the heading.

Also create a level 2 heading "Install script".
Create a "install_app" shell script in code block with the necessary command-line instructions to set up the project locally.
Ensure you start the install script by creating and changing to an app folder. Create folder name from the level 2 heading with name of app created in the prior step.
If the app requires any specific libraries or packages, please include the installation commands for those packages in the script.

Create a level 2 heading "Run script".
Create a "run_app" shell script with in code block with necessary command-line instructions to run the project locally.

Do not explain your response or generate any code comments.