## NavamAI to Streamlit

Your job is to create Streamlit app based on code from a module of navamai package.

Think step by step to create a user friendly, pleasing, and interactive app.

1. Study module code and functionality as below:

{{TEXT_FILE}}

2. Read the NavamAI API Documentation.
3. Think of how to represent the module code as features in the app.
4. Think about enabling the same functionality as provided by this module while importing and using the navamai package API.
5. Think of appropriate structure for user experience.
6. Think of appropriate streamlit UI components to use to bring the interactivity.
7. Think about how any data will be hydrated efficiently for a local running app.
8. Think about how to visualize such data in the app.
9. Use from the list of following libraries based on the app requirements:
    navamai
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
10. Create an app naming it by same name as the module.


Generate code for the entire app page as a markdown formatted response with separate code blocks for each file. Each code block should be preceded with a level 2 heading - File: file-name.ext. 

Start the response with a level 2 heading with name of the app based on the code provided. Add the description of the functionality below the heading.

Also create a level 2 heading "Install script".
Create a "install_app" shell script in code block with the necessary command-line instructions to set up the project locally.
Setup the multi-page streamlit app in a new folder named after the given module. Change to this folder.
Now create the main script within this folder.
Setup the python venv environment. If the app requires any specific libraries or packages, please include the installation commands for those packages in the script.

Create a level 2 heading "Run script".
Create a "run_app" shell script with in code block with necessary command-line instructions to run the main.py locally.

Do not explain your response or generate any code comments.

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