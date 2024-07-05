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

Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:
pip install rasa



yourproject/
├── actions/
│   └── actions.py
├── data/
│   ├── nlu.yml
│   ├── stories.yml
│   └── rules.yml
│
├── models/
├── tests/
│   └── test_stories.yml
├── config.yml
├── credentials.yml
├── endpoints.yml
├── README.md
└── domain.yml

actions/: Contains custom action implementations.
data/: Contains training data (NLU, stories, rules) and domain configuration.
models/: Directory where trained models are stored.
tests/: Contains test stories for testing the bot.
config.yml: Configuration file for the Rasa pipeline and policies.
credentials.yml: Contains credentials for external services.
endpoints.yml: Configuration for the action server and other endpoints.


Training Data
The training data is stored in the data/ directory.

NLU Data (nlu.yml): Contains intents, entities, and example training data.
Stories (stories.yml): Defines the conversation paths the bot can take.
Rules (rules.yml): Defines the rules for the bot's behavior.
Domain (domain.yml): Defines the intents, entities, slots, responses, actions, and forms used by the bot.

Running the Project

Train the model:
rasa train

Run the action server:
rasa run actions

Run the Rasa server:
rasa


Interacting with the Model
You can interact with your bot in the shell:
rasa shell

To test the bot with test stories:
rasa test