Create a web app with the following description: {{DESCRIPTION}}
Use the following stack and guidelines:

Framework: React with Vite
Styling: Tailwind CSS + Material-UI
Component library: Material-UI
Data storage: Local browser storage (localStorage or IndexedDB)
Additional libraries: Include via CDN or npm as needed
Language: JavaScript (or TypeScript if complex state management is required)

Provide key code snippets for the main functionality, including:
1. App.jsx (or App.tsx) as the main component
2. Any crucial custom components
3. State management setup (using React hooks)
4. Local data storage implementation

Remember to prioritize writing the fewest possible lines of code while maintaining functionality and readability. Utilize Tailwind CSS for styling and Material-UI components where appropriate to minimize custom CSS.
Ensure all functionality runs locally in the browser without requiring any cloud services.

Generate code for the entire app as a markdown formatted response with separate code blocks for each file. Each code block should be preceded with a level 2 heading - File: file-name.ext. 

Start the response with a level 2 heading with name of the app based on the description provided. Add the description as provided below the heading.

Also create a level 2 heading "Install script".
Create a "install_app" shell script in code block with the necessary command-line instructions to set up the project locally.
Ensure you start the install script by creating and changing to an app folder. Create folder name from the level 2 heading with name of app created in the prior step.
If the app requires any specific Material-UI components, please include the installation commands for those components in the script.
If the app requires any specific package imports, please include the installation commands for those NPM packages in the script.

Create a level 2 heading "Run script".
Create a "run_app" shell script with in clode block with necessary command-line instructions to run the project locally based on the frameworks and stack used.

Do not explain your response or generate any code comments.