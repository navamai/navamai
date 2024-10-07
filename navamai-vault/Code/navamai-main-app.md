## NavamAI App

This Streamlit multi-page app provides an interactive documentation landing page for NavamAI. It showcases the features, capabilities, and benefits of NavamAI through various interactive components and visualizations.

## Install script

```bash
#!/bin/bash

# Create and navigate to the navamai folder
mkdir navamai
cd navamai

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install streamlit streamlit-extras streamlit-option-menu streamlit-lottie pandas plotly requests

# Create the main script and pages folder
touch main.py
mkdir pages

# Deactivate the virtual environment
deactivate

echo "NavamAI app setup complete!"
```

## Run script

```bash
#!/bin/bash

# Navigate to the navamai folder
cd navamai

# Activate the virtual environment
source venv/bin/activate

# Run the Streamlit app
streamlit run main.py

# Deactivate the virtual environment when done
# deactivate
```

## File: main.py

```python
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="NavamAI Documentation", page_icon="🤖", layout="wide")

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    st.title("NavamAI Documentation")

    lottie_ai = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_kyu7xb1v.json")
    st_lottie(lottie_ai, height=200, key="ai_animation")

    st.markdown(
        """
        Welcome to the interactive documentation for NavamAI! This app will guide you through the features, 
        capabilities, and benefits of NavamAI, a powerful tool for supercharging your productivity and workflow 
        with personal, fast, and quality AI.
        """
    )

    selected = option_menu(
        menu_title=None,
        options=["Overview", "Features", "Commands", "Workflows", "Models"],
        icons=["house", "list-check", "terminal", "diagram-3", "cpu"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Overview":
        st.header("Overview")
        st.markdown(
            """
            NavamAI turns your Terminal into a configurable, interactive, and unobtrusive personal AI app. 
            With the power of 15 LLMs and 7 providers at your fingertips, NavamAI integrates seamlessly with 
            workflows in Markdown, VS Code, Obsidian, and GitHub.

            Get productive fast with three simple commands:
            ```bash
            pip install -U navamai
            navamai init
            ask "How can I use NavamAI?"
            ```
            """
        )

    elif selected == "Features":
        st.header("Key Features")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Command-Driven Interface")
            st.markdown("Interact with AI models using simple terminal commands.")
            st.subheader("Multiple Models and Providers")
            st.markdown("Access 15+ models from 7 different providers.")
        with col2:
            st.subheader("Markdown Workflow Integration")
            st.markdown("Seamlessly integrate with popular tools like VS Code and Obsidian.")
            st.subheader("Customizable and Extensible")
            st.markdown("Tailor NavamAI to suit your specific workflow needs.")

    elif selected == "Commands":
        st.header("NavamAI Commands")
        commands = {
            "ask": "Prompt the LLM for a fast, crisp response",
            "image": "Generate images based on prompts",
            "refer": "Process documents or prompts using specific configurations",
            "navamai init": "Initialize NavamAI in the current directory",
            "navamai config": "Edit the NavamAI configuration",
            "navamai test": "Test NavamAI commands across models and providers",
        }
        for cmd, desc in commands.items():
            st.markdown(f"**`{cmd}`**: {desc}")

    elif selected == "Workflows":
        st.header("NavamAI Workflows")
        st.markdown(
            """
            NavamAI supports various workflows to enhance your productivity:
            - Content expansion and generation
            - Multi-model comparisons
            - Intent-driven task execution
            - Validation of generated content
            """
        )
        st.image("https://raw.githubusercontent.com/navamai/navamai/main/images/navamai-intents-workflow.webp")

    elif selected == "Models":
        st.header("Supported Models and Providers")
        providers = ["Ollama", "Anthropic", "OpenAI", "Groq", "Google", "Bedrock", "Perplexity"]
        models = ["GPT-4", "Claude 3", "Gemini Pro", "Llama 2", "Mistral", "DALL-E"]
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Providers")
            for provider in providers:
                st.markdown(f"- {provider}")
        with col2:
            st.subheader("Notable Models")
            for model in models:
                st.markdown(f"- {model}")

if __name__ == "__main__":
    main()
```

## File: pages/quick_start.py

```python
import streamlit as st

def main():
    st.title("Quick Start Guide")

    st.markdown(
        """
        Get started with NavamAI in just a few simple steps:

        1. Install NavamAI:
        ```bash
        pip install -U navamai
        ```

        2. Initialize NavamAI in your desired folder:
        ```bash
        navamai init
        ```

        3. Identify the active provider and model:
        ```bash
        navamai id
        ```

        4. Start prompting the model:
        ```bash
        ask "How old is the oldest pyramid?"
        ```

        That's it! You're now ready to use NavamAI and explore its powerful features.
        """
    )

    st.subheader("Model Setup")
    st.markdown(
        """
        To use different models and providers, you'll need to set up API keys. Edit your environment config 
        (e.g., `~/.zshrc`) and add the following lines:

        ```bash
        export ANTHROPIC_API_KEY=your_key_here
        export OPENAI_API_KEY=your_key_here
        export GROQ_API_KEY=your_key_here
        export GEMINI_API_KEY=your_key_here
        export PERPLEXITY_KEY=your_key_here
        ```

        For local models, install [Ollama](https://ollama.com/) and download the models you want to use.
        """
    )

    st.subheader("Testing Models")
    st.code("navamai test ask", language="bash")
    st.code("navamai test vision", language="bash")

if __name__ == "__main__":
    main()
```

## File: pages/command_reference.py

```python
import streamlit as st
import pandas as pd

def main():
    st.title("NavamAI Command Reference")

    commands = [
        ("ask", "Prompt the LLM for a fast, crisp response"),
        ("audit", "Analyze NavamAI usage over time"),
        ("config", "Edit NavamAI configuration"),
        ("gather", "Scrape and save webpage content as markdown"),
        ("id", "Identify current provider and model"),
        ("image", "Generate images based on prompts"),
        ("init", "Initialize NavamAI in the current directory"),
        ("intents", "Process intents from a document or template"),
        ("merge", "Merge two files based on placeholders"),
        ("refer", "Process documents or prompts using specific configurations"),
        ("run", "Process and run code blocks from markdown files"),
        ("split", "Split large text files into smaller chunks"),
        ("test", "Test NavamAI commands across models and providers"),
        ("trends", "Visualize latency and token length trends"),
        ("validate", "Validate generated content using another model"),
        ("vision", "Process images using vision models"),
    ]

    df = pd.DataFrame(commands, columns=["Command", "Description"])
    st.dataframe(df, use_container_width=True)

    st.markdown(
        """
        For detailed usage of each command, use the `--help` option with the command. For example:
        ```bash
        navamai ask --help
        ```
        """
    )

if __name__ == "__main__":
    main()
```

## File: pages/workflows.py

```python
import streamlit as st

def main():
    st.title("NavamAI Workflows")

    st.markdown(
        """
        NavamAI supports various workflows to enhance your productivity and creativity. Here are some key workflows:
        """
    )

    st.header("Content Expansion")
    st.markdown(
        """
        Use NavamAI to expand partial content, seed ideas, or incomplete notes into full-fledged articles, blog posts, or research papers.

        1. Write partial content or seed ideas in a markdown file.
        2. Use the `refer` command to expand the content:
        ```bash
        refer post-to-update "your-file-name"
        ```
        3. NavamAI will process the content and generate an expanded version.
        """
    )

    st.header("Intent-Driven Workflow")
    st.markdown(
        """
        Create and expand on sets of intents and prompts to generate structured content:

        1. Define a document template with intents and prompts.
        2. Use the `refer` command to expand on the intents:
        ```bash
        refer intents-to-expand "Your Template Name"
        ```
        3. Use the `navamai intents` command to generate content for specific intents:
        ```bash
        navamai intents "Your Template Name"
        ```
        """
    )
    st.image("https://raw.githubusercontent.com/navamai/navamai/main/images/navamai-intents-workflow.webp")

    st.header("Multi-Model Comparison")
    st.markdown(
        """
        Compare responses from multiple models side by side:

        1. Open multiple terminal instances.
        2. In each terminal, set a different model:
        ```bash
        navamai config ask model model_name
        ```
        3. Run the same prompt across all terminals:
        ```bash
        ask "Your prompt here"
        ```
        4. Compare the results side by side.
        """
    )

    st.header("Content Validation")
    st.markdown(
        """
        Validate generated content using a different model:

        1. Generate content using one model.
        2. Use the `validate` command to check the content with another model:
        ```bash
        navamai validate "Your Template Name"
        ```
        3. NavamAI will provide a similarity score and highlight differences.
        """
    )

if __name__ == "__main__":
    main()
```

## File: pages/model_comparison.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("Model Comparison")

    st.markdown(
        """
        NavamAI allows you to compare different models and providers easily. Use the `navamai test` command 
        to run tests across all configured models and providers.
        """
    )

    # Sample data for demonstration purposes
    data = {
        "Model": ["GPT-4", "Claude 3", "Gemini Pro", "Llama 2", "Mistral"],
        "Provider": ["OpenAI", "Anthropic", "Google", "Meta", "Mistral AI"],
        "Latency (ms)": [250, 300, 200, 150, 180],
        "Token Count": [1500, 1800, 1600, 1400, 1300],
        "Accuracy (%)": [95, 93, 92, 90, 91],
    }

    df = pd.DataFrame(data)

    st.subheader("Model Performance Comparison")
    st.dataframe(df, use_container_width=True)

    st.subheader("Latency Comparison")
    fig_latency = px.bar(df, x="Model", y="Latency (ms)", color="Provider", title="Model Latency Comparison")
    st.plotly_chart(fig_latency, use_container_width=True)

    st.subheader("Token Count Comparison")
    fig_tokens = px.bar(df, x="Model", y="Token Count", color="Provider", title="Model Token Count Comparison")
    st.plotly_chart(fig_tokens, use_container_width=True)

    st.subheader("Accuracy Comparison")
    fig_accuracy = px.bar(df, x="Model", y="Accuracy (%)", color="Provider", title="Model Accuracy Comparison")
    st.plotly_chart(fig_accuracy, use_container_width=True)

    st.markdown(
        """
        To run your own model comparison tests, use the following command:
        ```bash
        navamai test ask
        ```
        This will run tests across all configured models and providers, allowing you to compare their performance.
        """
    )

if __name__ == "__main__":
    main()
```