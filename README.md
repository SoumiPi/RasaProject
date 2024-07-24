
# Rasa NLU Project

This project uses Rasa NLU for building conversational AI. Rasa NLU provides the natural language understanding (NLU) component of the system, enabling it to understand user inputs.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Training Data](#training-data)
- [Custom Actions](#custom-actions)
- [Running the Project](#running-the-project)
- [Interacting with the Model](#interacting-with-the-model)
- [Testing and Evaluation](#testing-and-evaluation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- pip (Python package installer)
- git (version control system)

## Installation

### Set Up a Virtual Environment

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source venv/bin/activate
     ```

### Install Rasa

3. **Install Rasa and its dependencies:**
   ```bash
   pip install rasa
   ```

### Initialize a Rasa Project

4. **Initialize a new Rasa project:**
   ```bash
   rasa init
   ```

## Project Structure

The project is organized as follows:

```plaintext
yourproject/
├── actions/
│  ├── actions_stock.py
│  ├── actions_achats.py
│  ├── actions_equip_transfer.py
│  └── actions_interventions.py
├── data/
│   ├── nlu.yml
│   ├── stories.yml
│   └── rules.yml
├── models/
├── tests/
│   └── test_stories.yml
├── config.yml
├── credentials.yml
├── endpoints.yml
├── README.md
├── domain.yml
├── app.py
└── static/
    ├── script.js
    ├── styles.css
    └── table_style.css
```

- **actions/**: Contains custom action implementations.
- **data/**: Contains training data (NLU, stories, rules) and domain configuration.
- **models/**: Directory where trained models are stored.
- **tests/**: Contains test stories for testing the bot.
- **config.yml**: Configuration file for the Rasa pipeline and policies.
- **credentials.yml**: Contains credentials for external services.
- **endpoints.yml**: Configuration for the action server and other endpoints.
- **domain.yml**: Defines the intents, entities, slots, responses, actions, and forms used by the bot.

## Training Data

The training data is stored in the `data/` directory.

- **NLU Data (`nlu.yml`)**: Contains intents, entities, and example training data.
- **Stories (`stories.yml`)**: Defines the conversation paths the bot can take.
- **Rules (`rules.yml`)**: Defines the rules for the bot's behavior.
- **Domain (`domain.yml`)**: Defines the intents, entities, slots, responses, actions, and forms used by the bot.

## Custom Actions

Custom actions are implemented in the `actions/` directory, specifically in the `actions.py` file. These actions allow the bot to perform specific tasks that require backend logic, such as querying a database or integrating with external APIs.

## Running the Project

1. **Train the model:**
   ```bash
   rasa train
   ```

2. **Run the action server:**
   ```bash
   rasa run actions
   ```

3. **Run the Rasa server:**
   ```bash
   rasa run
   ```

## Interacting with the Model

You can interact with your bot using the command line interface:

- **To chat with your bot in the shell:**
  ```bash
  rasa shell
  ```

- **To test the bot with test stories:**
  ```bash
  rasa test
  ```

## Testing and Evaluation

To ensure the quality of your bot, it’s crucial to test it. Use the `rasa test` command to run test stories defined in `tests/test_stories.yml`. This will validate the bot's responses and provide metrics on its accuracy.

## Deployment

Details on how to deploy your Rasa bot can be added here, including server setup, Docker configuration, and CI/CD pipeline integration.

## Contributing

Guidelines for contributing to the project can be provided here, including how to fork the repository, make changes, and submit pull requests.

## License

Specify the project's licensing information here, including any open-source licenses used.
```

In this format, the Table of Contents (TOC) should link directly to the respective sections when clicked. The header IDs in the TOC (like `#prerequisites`) must exactly match the generated IDs from the section headings. If you continue to experience issues, it could be related to the specific Markdown renderer or viewer you are using. Some renderers might handle links differently, especially if there are special characters or casing differences.