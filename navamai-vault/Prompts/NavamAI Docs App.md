# NavamAI App

Your job is to create a Streamlit multi-page app with main.py main script and required app pages in pages folder.

Think step by step to create a user friendly, pleasing, interactive documentation landing page.
1. Read the NavamAI README and API Documentation.
2. Think of how to best present the features, capabilities, and benefits of NavamAI.
3. Think of appropriate structure for the interactive documentation.
4. Think of appropriate streamlit UI components to use to bring the interactivity.
5. Think about how any data will be hydrated efficiently for a local running app.
6. Think about how to visualize such data in the app.
7. Use from the list of following libraries based on the app requirements:
    streamlit-extras
    streamlit-aggrid
    plotly
    altair
    matplotlib
    seaborn
    bokeh
    pydeck
    streamlit-option-menu
    streamlit-lottie
    streamlit-folium
    streamlit-ace
    streamlit-authenticator
    streamlit-bokeh-events
    streamlit-elements
    pandas
    numpy
    scipy
    scikit-learn
    tensorflow  # or pytorch
    requests
    streamlit-gsheets
    streamlit-autorefresh
    streamlit-camera-input-live
    streamlit-toggle-switch
    streamlit-embedcode
8. Create the landing page.


Generate code for the entire muli-page app as a markdown formatted response with separate code blocks for each file. Each code block should be preceded with a level 2 heading - File: file-name.ext. 

Start the response with a level 2 heading with name of the app based on the code provided. Add the description of the functionality below the heading.

Also create a level 2 heading "Install script".
Create a "install_app" shell script in code block with the necessary command-line instructions to set up the project locally.
Setup the multi-page streamlit app in a new folder name navamai. Change to this folder.
Now create the main script within navamai folder.
Setup the python venv environment. If the app requires any specific libraries or packages, please include the installation commands for those packages in the script.

Create a level 2 heading "Run script".
Create a "run_app" shell script with in code block with necessary command-line instructions to run the main.py locally.

Do not explain your response or generate any code comments.

# NavamAI README

Use NavamAI to supercharge your productivity and workflow with personal, fast, and quality AI. Turn your Terminal into a configurable, interactive, and unobtrusive personal AI app. Power of 15 LLMs and 7 providers at your finger tips. Pair with workflows in Markdown, VS Code, Obsidian, and GitHub. Get productive fast with three simple commands.

[![](https://raw.githubusercontent.com/navamai/navamai/main/images/navamai-youtube.png)](https://www.youtube.com/watch?v=rnKpeChON3g)

**Command Is All You Need:** So, the LLM science fans will get the pun in our tagline. It is a play on the famous paper that introduced the world to Transformer model architecture - Attention is all you need. With NavamAI a simple command via your favorite terminal or shell is all you need to bend an large or small language model to your wishes. NavamAI provides a rich UI right there within your command prompt. No browser tabs to open, no apps to install, no context switching... just pure, simple, fast workflow. Try it with a simple command like `ask "create a table of planets"` and see your Terminal come to life just like a chat UI with fast streaming responses, markdown formatted tables, and even code blocks with color highlights if your prompt requires code in response! NavamAI has released 14 commands to help customize your personal AI workflow.

**Top Models and Providers:** You can switch private models or hosted frontier LLMs with ease. NavamAI comes with configurable support for more than 15 leading models (GPT 4o, Sonnet 3.5, Gemini 1.5 Pro, Mistral NeMo, Sonar Llama 3.1...) from 7 providers (Ollama, Anthropic, OpenAI, Groq, Google, Bedrock, and Perplexity).

**Markdown Workflows:** NavamAI works with markdown content (text files with simple formatting commands). So you can use it with many popular tools like VS Code and Obsidian to quickly and seamlessly design a custom workflow that enhances your craft.

**Do More With Less:** NavamAI is very simple to use out of the box as you learn its handful of powerful commands. As you get comfortable you can customize NavamAI commands simply by changing one configuration file and align NavamAI to suit your workflow. Everything in NavamAI has sensible defaults to get started quickly. 

**Make It Your Own:** When you are ready, everything is configurable and extensible including commands, models, providers, prompts, model parameters, folders, and document types. Another magical thing happens when the interface to your generative AI is a humble command prompt. You will experience a sense of being in control. In control of your workflow, your privacy, your intents, and your artifacts. You are completely in control of your personal AI workflow with NavamAI.

## Quick Start

Go to a folder where you want to initialize NavamAI. This could be your Obsidian vault or a VC Code project folder or even an empty folder.

```bash
pip install -U navamai # upgrade or install latest NavamAI
navamai init # copies config file, quick start samples
navamai id # identifies active provider and model
ask "How old is the oldest pyramid?" # start prompting the model
```

### Models Setup
You will need to setup model-provider keys. Edit your environment config `~/.zshrc` like so.

```bash
export ANTHROPIC_API_KEY= # https://docs.anthropic.com/en/api/getting-started
export OPENAI_API_KEY= # https://openai.com/index/openai-api/
export GROQ_API_KEY= # https://console.groq.com/keys
export GEMINI_API_KEY= # https://ai.google.dev/gemini-api
export PERPLEXITY_KEY= # https://www.perplexity.ai/settings/api
```

If you do not want to use any of the model then all you need to do is remove the corresponding entries from `navamai.yml` in the `model-mapping` and the `provider-model-mapping` sections. Also ensure that the other model configs only refer to available models.

For local models [install Ollama](https://ollama.com/) and download the latest [models](https://ollama.com/library) you want to run.

Now you are ready to test all models and providers.

```bash
navamai test ask
navamai test vision
```

### Python Environment Setup (optional)

*Skip this section if you have your Python environment already working.*

First, you should be running the latest Python on your system with Python package manager upgraded to the latest.

```bash
python --version
# should return Python 3.12.x or higher as on Sep'24
```

1. Optionally install latest [Python on Mac](https://docs.python-guide.org/starting/install3/osx/). 
2. Safely install NavamAI. Follow [this thread](https://apple.stackexchange.com/questions/237430/how-to-install-specific-version-of-python-on-os-x) to setup `pyenv` version manager.

First change to the directory to your VS Code workspace, Obsidian vault, or folder where you want to install NavamAI. Next create the virtual environment.

```bash
python -m venv env
```

Now you can activate your virtual environment like so. You will notice that directory prefixed with `(env)` to indicate you are now running in the virtual environment.

```bash
. env/bin/activate
```

To leave the virtual environment using `deactivate` command. Re-enter using same command as earlier.

Now you are ready to install NavamAI.

## Command Reference

*Note that `navamai`, `ask`, `image` and `refer` are four top level commands available to you when you install NavamAI.

| Command      | Example and Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ***ask**     | `ask "your prompt"`<br>Prompt the LLM for a fast, crisp (default up to 300 words), single turn response<br><br>`ask`<br>Browses the configured prompts folder, lists prompt templates for user to run.                                                                                                                                                                                                                                                                                                                   |
| **audit**    | `navamai audit`<br>Analyze your own usage of NavamAI over time with an insightful command line dashboard and markdown report.                                                                                                                                                                                                                                                                                                                                                                                            |
| **config**   | `navamai config ask save true`<br>Edit `navamai.yml` file config from command line                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **gather**   | `navamai gather "webpage url"`<br>Cleanly scrape an article from a webpage, without the menus, sidebar, footer. Includes images. Saves as markdown formatted similar to the HTML source.<br> <br>Refer the scraped markdown content using `refer gather` command.<br>Use vision on scraped images using `navamai vision` command.                                                                                                                                                                                        |
| ***refer**   | `refer text-to-extract`<br>Browse a set of raw text files and run custom prompts to extract new structured content.<br><br>`refer inline-prompts-to-run`<br>Run prompts embedded inline within text to expand, change, and convert existing documents.<br><br>`refer intents`<br>Expand a set of intents and prompts within an intents template<br><br>`refer your-command`<br>You can configure your own extensions to refer command by simply copying and changing any of the existing `refer-existing` model configs. |
| **run**      | `navamai run`<br>Browse `Code` folder for markdown files with code blocks, create, setup, and run the app in one single command!<br><br>The `Code` folder markdown files with code blocks are created using `ask` command running `Create Vite App.md` prompt template or similar.                                                                                                                                                                                                                                       |
| **id**       | `navamai id`<br>Identifies the current provider and model for `ask` command<br><br>`navamai id section-name`<br>Identifies the provider and model defined in specific section                                                                                                                                                                                                                                                                                                                                            |
| ***image**   | `image`<br>Select a prompt template to generate an image.<br><br>`image "Prompt for image to generate"`<br>Prompt to generate an image.                                                                                                                                                                                                                                                                                                                                                                                  |
| **init**     | `navamai init`<br>Initialize navamai in any folder. Copies `navamai.yml` default config and quick start Intents and Embeds folders and files. Checks before overwriting. Use --force option to force overwrite files and folders.                                                                                                                                                                                                                                                                                        |
| **intents**  | `navamai intents "Financial Analysis"`<br>Interactively choose from a list of intents within a template to refer into content embeds                                                                                                                                                                                                                                                                                                                                                                                     |
| **merge**    | `navamai merge "Source File"`<br>Finds `Source File updated` with placeholder tags `[merge here]` or as custom defined in `merge` config, then merges the two files into `Source File merged`. Use along with `refer inline-prompts-to-run` command to reduce number of tokens processed when editing long text for context but updating only a section.                                                                                                                                                                 |
| **split**    | `navamai split "Large File"`<br>Use this command to split a large file into chunks within a specified ratio of target model context. You can configure target model and ratio in `split` section of the configuration. Original file remains untouched and new files with same name and `part #` suffix are created.                                                                                                                                                                                                     |
| **test**     | `navamai test ask`<br>Tests navamai command using all providers and models defined in `navamai.yml` config and provides a test summary.<br><br>`navamai test vision`<br>Test vision models.                                                                                                                                                                                                                                                                                                                              |
| **trends**   | `navamai trends`<br>Visualize latency and token length trends based on `navamai test` runs for `ask` and `vision` commands across models and providers. You can trend for a period of days using  `--days 7` command option.                                                                                                                                                                                                                                                                                             |
| **validate** | `navamai validate "Financial Analysis"`<br>Validates prior generated embeds running another model and reports the percentage difference between validated and original content.                                                                                                                                                                                                                                                                                                                                          |
| **vision**   | `navamai vision -p path/to/image.png "Describe this image"`<br>Runs vision models on images from local path (-p), url (-u), or camera (-c) and responds based on prompt.                                                                                                                                                                                                                                                                                                                                                 |


## NavamAI Expands Your Content

Using NavamAI with few simple commands in your Terminal you can create a simple yet powerful personal AI content manager with your Markdown tool of choice like Obsidian or VS Code. For example, you can write partial blogs posts, write your seed ideas, start with a list of intents and prompts, or capture partial notes from a lecture where you were slightly distracted. 

Then you can use `refer` command in conjunction with custom `refer-section` configs within `navamai.yml` to expand this partial, incomplete, or seed content into complete posts, notes, articles, prompt templates, and even well-researched papers. You can experiment with choice of models and providers, tune model settings in the config by document type, define custom folders for your content, and specify document specific system prompts to get exactly the outcome you desire based on the type of the document. You just have to remember one simple command `refer` and you are all set.

As a quick example, check out the `Posts` folder with sample partially written post on startup growth strategies. Now view the related config section within `navamai.yml` for expanding posts.

```yaml
refer-post-to-update:
  lookup-folder: Posts
  max-tokens: 4000
  model: sonnet
  provider: claude
  save: true
  save-folder: Posts
  system: You will be given a partially written blog post on a topic.
    Your job as an expert blog writer is to expand the post...
  temperature: 0.5
```

Please note that for brevity we are not listing the complete system prompt here. You can obviously change it to suit your workflow. For now, just run `refer post-to-update "startup-growth-hacking"` command within the working folder where you initialized NavamAI. Soon the model response starts streaming into your terminal. The expanded post is saved in the `Posts` folder with `updated` prefix so you can compare with the original.

To create a new document type like research papers, class notes, cooking recipes, or whatever, all you need to do is copy and customize one of the `refer-post-to-update` or `refer-intents-to-expand` sections into something like your custom `refer-notes-to-summarize` section. Then you can run a custom command on your new document type like `refer notes-to-summarize "your-notes-file"` and achieve the same results.

## Combining NavamAI Commands

When combined with other NavamAI commands this workflow can get even more powerful. As an example, start by defining your document template for a set of intents and prompts as a simple markdown. For example `Financial Analysis` or `Product Management` are shown here. Next add a few intents as headings like, `Macro Factors Impact Stocks` or `Top Companies by ROCE` and so on. Then add simple prompts under these intents to generate content. You can now use NavamAI to expand on the set of intents and prompts in your document template with the command `refer intents-to-expand "Financial Analysis"` and the model will brainstorm more related intents and prompts for you to use.

![](https://raw.githubusercontent.com/navamai/assets/main/images/obsidian-navamai.png)

Now run `navamai intents-to-expand "Financial Analysis"` and choose among a list of intents to generate as content embeds. The response is saved under `Embeds` folder automatically and the embed is linked in your document template instantly. Rinse, repeat.

This workflow can get really useful very fast. As each template has linked embeds, Obsidian Graph view can be used to visualize the links. You can get creative and link related templates or even enhance generated embeds with more intents. Of course this also means you can use all the great Obsidian plugins to generate websites, PDFs, and more.  Your creativity + Obsidian + NavamAI = Magic!

![](https://raw.githubusercontent.com/navamai/navamai/main/images/navamai-intents-workflow.webp)


## Test and Evaluate Models and Providers

NavamAI comes with configurable support for more than 15 leading models from five providers (Ollama, Anthropic, OpenAI, Groq, Google). The `navamai test` command can be used to run each of the navamai commands over all the provider and model combinations and respond with a summary of model test and evaluation results. Use this to quickly compare models and providers as well as when you add or remove a new model or provider in the config.

This command is super useful when comparing model response time (latency), response quality (does it follow the system and prompt instructions), response accuracy, and token length (cost) for the same prompt. You can configure the test prompts within `navamai.yml` in the `test` section.

![](https://raw.githubusercontent.com/navamai/navamai/main/images/test-summary.webp)

Here is an example of running `navamai test vision` command and resulting test summary. I this default prompt and image we are sharing image of around 150-160 people standing in close proximity in a circle and asking the model to count the number of people. The right number is between 150-160. This can be used to calculate the relative accuracy of each model based on the response. How closely the response follows the system prompt and the user prompts is  indicative of quality of response.

You can also notice the response times seem proportional to model size. For Claude, Opus > Sonnet > Haiku. For Gemini, Pro > Flash. For OpenAI, GPT-4o > GPT-4-mini.

You can similarly run `navamai test ask` command to test across all models and providers. In this run you may find groq is among the fastest providers when it comes to response time.

Of course, you may need multiple test runs to get better intuition of response times as there are multiple factors which effect latency other than model size or architecture, like network latency, which may change across multiple test runs.

## Visualize Trends

Each `navamai test` command run saves the test summary data in `Metrics` folder by timestamp and provider-model. Over time you can visualize trends of latency and token count metrics to see if models are performing consistently. Run `navamai trends` command to view trends for 7 days (default).

![](https://raw.githubusercontent.com/navamai/navamai/main/images/trends.webp)

The visualization uses sparklines to show data trends over time. Use this to decide when/if to switch models based on performance trends.

## Run multiple models side by side

Want to compare multiple models side by side? All you need to do is open multiple shells or Terminal instances. Now in each of these, one by one, change the model, run same `ask "prompt"` and compare the results side by side. Simple!

![](https://raw.githubusercontent.com/navamai/assets/main/images/compare-models-1.png)

![](https://raw.githubusercontent.com/navamai/assets/main/images/compare-models-2.png)

As NavamAI commands use the `navamai.yml` config in the current folder every time they run, you can create more complex parallel running, multi-model and cross-provider workflows by simply copying the config file into multiple folders and running commands there. This way you can be running some long running tasks on a local model in one folder and terminal. While you are doing your day to day workflow in another. And so on.


## Workflow freedom

There is no behavioral marketing or growth hacking a business can do within your command prompt. You guide your workflow the way you feel fit. Run the fastest model provider (Groq with Llama 3.1), or the most capable model right now (Sonnet 3.5 or GPT-4o), or the latest small model on your laptop (Mistral Nemo), or the model with the largest context (Gemini 1.5 Flash), you decide. Run with fast wifi or no-wifi (using local models), no constraints. Instantly search, research, Q&A to learn something or generate a set of artifacts to save for later. Switching to any of these workflows is a couple of changes in a config file or a few easy to remember commands on your terminal.

You can also configure custom model names to actual model version mapping for simplifying model switching commands. With the following mapping the commands to switch models are `navamai config ask model llama` or `navamai config intents model haiku` and so on.

```yaml
model-mapping:
  # Claude models
  sonnet: claude-3-5-sonnet-20240620
  opus: claude-3-opus-20240229
  haiku: claude-3-haiku-20240307
  
  # Ollama models
  llama: llama3.1
  gemma: gemma2
  mistral: mistral-nemo
  
  # Groq models
  groq-mixtral: mixtral-8x7b-32768
  groq-llama: llama2-70b-4096

  # OpenAI models
  gpt4mini: gpt-4o-mini
  gpt4o: gpt-4o

  # Gemini models
  gemini-pro: gemini-1.5-pro
  gemini-flash: gemini-1.5-flash
```



## Privacy controls 

You decide which model and provider you trust, or even choose to run an LLM locally on your laptop. You are in control of how private your data and preferences remain. NavamAI supports state of the art models from Anthropic, OpenAI, Google, and Meta. You can choose a hosted provider or Ollama as a local model provider on your laptop. Switch between models and providers using a simple command like `navamai config ask model llama` to switch from the current model.

You can also load custom model config sets mapped to each command. Configure these in `navamai.yml` file. Here is an example of constraining how `navamai ask` and `navamai intents` commands behave differently using local and hosted model providers.

```yaml
ask:
  provider: ollama
  model: mistral
  max-tokens: 300
  save: false
  system: Be crisp in your response. Only respond to the prompt 
	using valid markdown syntax. Do not explain your response.
  temperature: 0.3

intents:
  provider: claude
  model: sonnet
  max-tokens: 1000
  save: true
  folder: Embeds
  system: Only respond to the prompt using valid markdown syntax.
    When responding with markdown headings start at level 2. 
    Do not explain your response.
  temperature: 0.0
```


## Audit Trail

NavamAI saves a trail of commands, prompts, templates, lookup folders, and saved files in `trail.yml` file. You can visualize this anytime using `navamai audit` command to gain insights of your NavamAI usage over time.

![](https://raw.githubusercontent.com/navamai/navamai/main/images/audit-summary.webp)

![](https://raw.githubusercontent.com/navamai/navamai/main/images/audit-prompt-analysis.webp)

## Intent driven 

Your intents are tasks you want to execute, goals you want to accomplish, plans you want to realize, decisions you want to make, or questions you want to answer. You control your entire NavamAI experience with your intents. You can save your intents as simple outline of tasks in a text file. You can recall them when you need. You can run models on your intents as you feel fit. You can save results based on your intents.

![](https://raw.githubusercontent.com/navamai/navamai/main/images/navamai-intents.webp)

## Validate Generations

You can verify content generated by one LLM with validation from another model. Make sure you only run validate command after you have run `refer intents` command to generate the first pass of embeds. Use `navamai validate "Financial Analysis"` or any intent template that you have created. The workflow for validation is similar to expand intents. Only in this case the validate model config decides which model and provider to use. You can also modify the validation prompt to check for any specific things relevant for your use case. The diff is calculated on original and validated text removing any newlines, white space, or markdown formatting when making the diff comparison using similarity scoring. Use this to automate quality validation of generated content.

# NavamAI API Documentation

NavamAI is a Python package that provides a command-line interface for interacting with various AI models and performing tasks such as text generation, image creation, and more. This documentation covers the API for using NavamAI within external projects.

## Table of Contents

1. [Installation](#installation)
2. [Command-Line Interface](#command-line-interface)
3. [Modules](#modules)
   - [claude](#claude)
   - [code](#code)
   - [configure](#configure)
   - [evaluate](#evaluate)
   - [gather](#gather)
   - [gemini](#gemini)
   - [generate](#generate)
   - [groq](#groq)
   - [images](#images)
   - [markdown](#markdown)
   - [metrics](#metrics)
   - [model_text](#model_text)
   - [model_vision](#model_vision)
   - [ollama](#ollama)
   - [openai](#openai)
   - [perplexity](#perplexity)
   - [provider](#provider)
   - [reference](#reference)
   - [utils](#utils)
   - [validation](#validation)

## Installation

To install NavamAI, use pip:

```bash
pip install -U navamai
```

## Command-Line Interface

NavamAI provides a command-line interface with various commands. Here's an overview of the available commands:

- `run`: Processes a selected markdown file and runs the code blocks within it.
- `audit`: Analyzes the usage of NavamAI over time and generates a report.
- `gather`: Scrapes content from a webpage and saves it as markdown.
- `split`: Splits a large text file into smaller chunks.
- `trends`: Visualizes trends for provider-model combinations.
- `test`: Tests the specified model configuration.
- `init`: Initializes NavamAI in the current directory.
- `config`: Edits the NavamAI configuration.
- `id`: Identifies the current provider and model for a given section.
- `image`: Generates an image based on a prompt or template.
- `ask`: Processes a prompt or template using the configured AI model.
- `refer`: Processes a document or prompt using a specified section of the configuration.
- `intents`: Processes intents from a document or template.
- `merge`: Merges two files based on placeholders.
- `validate`: Validates generated content using another model.
- `vision`: Processes an image using vision models and responds based on a prompt.

For detailed usage of each command, please refer to the CLI documentation or use the `--help` option with each command.

## Modules

### claude

The `claude` module provides a `Claude` class that interacts with the Anthropic API for text and vision tasks.

#### Class: `Claude`

```python
class Claude(Provider):
    def __init__(self):
        # Initialize the Claude provider
    
    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # Stream a response for a given text prompt
    
    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str = None) -> Generator[str, None, None]:
        # Stream a response for a given image and text prompt
```

### code

The `code` module provides functionality for processing markdown files and running code blocks.

#### Functions:

```python
def process_markdown_file(file_path: str, app_folder: str):
    # Process a markdown file, extract code blocks, and run them
```

### configure

The `configure` module handles configuration management for NavamAI.

#### Functions:

```python
def load_config(section: Optional[str] = None) -> Dict[str, Any]:
    # Load the configuration from navamai.yml

def has_vision_capability(model: str) -> bool:
    # Check if a model has vision capabilities

def save_config(config: Dict[str, Any]):
    # Save the configuration to navamai.yml

def edit_config(keys: List[str], value: Any):
    # Edit a specific configuration value

def get_model_mapping() -> Dict[str, str]:
    # Get the model mapping from the configuration

def resolve_model(model: str) -> str:
    # Resolve a model name to its actual identifier
```

### evaluate

The `evaluate` module provides functionality for evaluating model configurations.

#### Functions:

```python
def by_model_config(model_config: str):
    # Evaluate the specified model configuration across all compatible providers and models
```

### gather

The `gather` module provides functionality for scraping web articles and saving them as markdown files.

#### Functions:

```python
def article(url: str) -> Optional[str]:
    # Scrape an article from the given URL and save it as a markdown file
    # Returns the path of the saved file or None if scraping failed
```

### gemini

The `gemini` module provides a `Gemini` class that interacts with the Google Generative AI API for text and vision tasks.

#### Class: `Gemini`

```python
class Gemini(Provider):
    def __init__(self):
        # Initialize the Gemini provider
    
    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # Stream a response for a given text prompt
    
    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str) -> Generator[str, None, None]:
        # Stream a response for a given image and text prompt
```

### generate

The `generate` module provides functionality for generating images using various AI providers.

#### Functions:

```python
def image(prompt: Optional[str], template: Optional[str]) -> Dict[str, Any]:
    # Generate an image based on a prompt or template
    # Returns a dictionary with information about the generated image

def _generate_image_with_progress(provider_instance: Provider, prompt: str, duration: int) -> str:
    # Generate an image with a progress bar
    # Returns the path of the generated image file
```

### groq

The `groq` module provides a `Groq` class that interacts with the Groq API for text-based tasks.

#### Class: `Groq`

```python
class Groq(Provider):
    def __init__(self):
        # Initialize the Groq provider
    
    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # Stream a response for a given text prompt
    
    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str) -> Generator[str, None, None]:
        # Raises NotImplementedError as Groq doesn't support vision-based responses
```

### images

The `images` module provides utility functions for handling images in NavamAI.

#### Functions:

```python
def display_image(image_path: str):
    # Display an image in the terminal (works best in VS Code Terminal)

def capture_image() -> bytes:
    # Capture an image from the camera and return it as bytes

def resize_image(image_data: bytes, max_size: int = 5 * 1024 * 1024) -> bytes:
    # Resize an image to ensure it's under a specified size (default 5MB)
    # Returns the resized image as bytes
```

### markdown

The `markdown` module provides utility functions for working with markdown files and text processing.

#### Functions:

```python
def split_text_by_tokens(file_path: str, model: str = "gpt-3.5-turbo") -> int:
    # Split a text file into chunks based on token count
    # Returns the number of chunks created

def extract_variables(template: str) -> List[str]:
    # Extract variables enclosed in double curly braces from a template string

def list_files(directory: str, page: int = 1, files_per_page: int = 10, extensions: Optional[List[str]] = None) -> Tuple[List[str], int]:
    # List files in a directory with pagination

def count_tokens(file_path: str) -> int:
    # Count the number of tokens in a file

def intent_select_paginate(sections: List[Tuple[str, str]], page: int = 1, intents_per_page: int = 10) -> Optional[Tuple[str, str]]:
    # Display a paginated list of intents for selection

def file_select_paginate(directory: str, show_tokens: bool = False, section: Optional[str] = None, extensions: Optional[List[str]] = None) -> Optional[str]:
    # Display a paginated list of files for selection

def merge_docs(source_path: str, dest_suffix: str = "expanded", merge_suffix: str = "merged", placeholder: str = "[merge here]", prompt_prefix: str = "> Prompt:"):
    # Merge two markdown documents based on placeholders

def diff(content1: str, content2: str) -> float:
    # Calculate the difference percentage between two content strings

def parse_markdown_sections(content: str) -> List[Tuple[str, str]]:
    # Parse markdown content into sections (title and prompt)

def update_markdown_with_response(filename: str, title: str, response_filename: str):
    # Update a markdown file with an Obsidian-flavored embed for a response
```

### metrics

The `metrics` module provides functions for tracking and analyzing metrics related to model performance.

#### Functions:

```python
def count_tokens(text: str) -> int:
    # Count the number of tokens in the given text

def save_test_summary(provider: str, model: str, model_config: str, prompt: str, status: str, details: str, response_time: float, token_count: int):
    # Save a test summary to a YAML file

def read_yaml_files(directory: str = "Metrics") -> Dict[str, Any]:
    # Read test summary YAML files from a directory

def process_data(data: Dict[str, Any], days: int = 7) -> Dict[Tuple[str, str, str], Dict[str, List[Any]]]:
    # Process test summary data for trend analysis

def display_trends(processed_data: Dict[Tuple[str, str, str], Dict[str, List[Any]]]):
    # Display trends for response times and token counts
```

### model_text

The `model_text` module handles text-based model interactions.

#### Functions:

```python
def process(prompt: Optional[str], template: Optional[str]) -> Dict[str, Any]:
    # Process a text prompt or template using the configured AI model
    # Returns a dictionary with information about the processed prompt and response
```

### model_vision

The `model_vision` module handles vision-based model interactions.

#### Functions:

```python
def process(path: Optional[str], url: Optional[str], camera: bool, display: bool, prompt: Optional[str]) -> Dict[str, Any]:
    # Process an image using vision models and respond based on a prompt
    # Returns a dictionary with information about the processed image and response
```

### ollama

The `ollama` module provides an `Ollama` class for interacting with locally hosted Ollama models.

#### Class: `Ollama`

```python
class Ollama(Provider):
    def __init__(self):
        # Initialize the Ollama provider
    
    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # Stream a response for a given text prompt
    
    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str) -> Generator[str, None, None]:
        # Stream a response for a given image and text prompt
```

Note: The Ollama provider does not support WebP image format for vision tasks.

### openai

The `openai` module provides an `Openai` class for interacting with OpenAI's API for text and image generation tasks.

#### Class: `Openai`

```python
class Openai(Provider):
    def __init__(self):
        # Initialize the OpenAI provider

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # Stream a response for a given text prompt

    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str) -> Generator[str, None, None]:
        # Stream a response for a given image and text prompt

    def generate_image(self, prompt: str) -> str:
        # Generate an image based on a text prompt
        # Returns the filepath of the generated image

    def save_image_response(self, prompt: str, image_data: bytes) -> str:
        # Save a generated image to a file
        # Returns the filepath of the saved image
```

### perplexity

The `perplexity` module provides a `Perplexity` class for interacting with the Perplexity AI API for text-based tasks.

#### Class: `Perplexity`

```python
class Perplexity(Provider):
    def __init__(self):
        # Initialize the Perplexity provider

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # Stream a response for a given text prompt

    def stream_vision_response(self, image_data: bytes, prompt: str) -> Generator[str, None, None]:
        # Not implemented for Perplexity (raises NotImplementedError)
```

### provider

The `provider` module defines an abstract `Provider` class that serves as a base for all AI provider implementations.

#### Class: `Provider`

```python
class Provider(ABC):
    def __init__(self):
        # Initialize the provider

    @abstractmethod
    def create_request_data(self, prompt: str) -> dict:
        # Create request data for the API call

    @abstractmethod
    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # Stream a response for a given text prompt

    @abstractmethod
    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: Optional[str] = None) -> Generator[str, None, None]:
        # Stream a response for a given image and text prompt

    def set_model_config(self, model_config: str):
        # Set the model configuration

    def ask(self, prompt: str, title: Optional[str] = None) -> Optional[str]:
        # Process a text prompt and optionally save the response

    def vision(self, image_data: bytes, prompt: str, title: Optional[str] = None):
        # Process an image prompt

    def save_response(self, prompt: str, response: str, title: Optional[str] = None) -> str:
        # Save a response to a file

    def get_model_info(self) -> str:
        # Get information about the current model

    def resolve_model(self, model: str) -> str:
        # Resolve the actual model name from the configuration
```

### reference

The `reference` module provides functionality for processing documents and prompts using specific configurations.

#### Functions:

```python
def process(section: str, document: Optional[str] = None, prompt: Optional[str] = None) -> Dict[str, Any]:
    # Process a document or prompt using a specified configuration section
    # Returns a dictionary with information about the processed document and response

def _document_prompt(config_section: str, document: Optional[str] = None, prompt: Optional[str] = None) -> Tuple[str, Optional[str], Optional[str]]:
    # Internal function to handle document selection and prompt processing
```

### utils

The `utils` module provides utility functions and decorators for the NavamAI package.

#### Functions:

```python
def trail(f):
    # Decorator to log command executions and their results

def get_provider_instance(provider: str) -> Provider:
    # Get an instance of the specified AI provider
```

### validation

The `validation` module provides functionality for validating generated content using another model.

#### Functions:

```python
def validate(document: Optional[str] = None) -> Dict[str, Any]:
    # Validate generated content using another model
    # Returns a dictionary with information about the validation process
```