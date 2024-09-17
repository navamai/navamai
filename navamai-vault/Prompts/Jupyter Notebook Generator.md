Create a Jupyter Notebook with the following description: {{DESCRIPTION}}
Use the following stack and guidelines:

Environment: Jupyter Notebook
Language: Python 3.x
Data manipulation: Pandas, NumPy
Visualization: Matplotlib, Seaborn, Plotly
Machine Learning: Scikit-learn
Deep Learning: TensorFlow or PyTorch (if required)
Natural Language Processing: NLTK or spaCy (if required)
Additional libraries: Include as needed for specific tasks

Provide key code cells for the main functionality, including:

Importing necessary libraries
Data loading and preprocessing
Exploratory Data Analysis (EDA) with visualizations
Model development and training (if applicable)
Results visualization and interpretation

Remember to prioritize writing clear, efficient code while maintaining functionality and readability. Utilize appropriate libraries for data manipulation, visualization, and analysis to minimize custom implementations.
Generate code for the entire notebook as a markdown formatted response with separate code blocks for each cell. Each code block should be preceded with a level 2 heading - Cell: cell-number.
Start the response with a level 2 heading with the name of the notebook based on the description provided. Add the description as provided below the heading.
Also create a level 2 heading "Environment Setup".
Create a "setup_environment.sh" shell script in a code block with the necessary command-line instructions to set up the project environment locally.
Ensure you start the script by creating and changing to a project folder. Create the folder name from the level 2 heading with the name of the notebook created in the prior step.
Include commands to create a virtual environment, activate it, and install all required packages.
Create a level 2 heading "Run Notebook".
Create a "run_notebook.sh" shell script in a code block with necessary command-line instructions to start the Jupyter Notebook server and open the notebook.
Do not explain your response or generate any code comments in the notebook cells.