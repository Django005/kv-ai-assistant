## Installation Steps

### Requirements
- Rasa only supports Python 3.9 and 3.10, so if another version of Python is installed on your device, install pyenv to manage and install multiple Python versions. A guide to using pyenv is towards the bottom of this README.
- There are two separate sections for instructions in this README: One for Windows systems, and one for MacOS systems.

### Instructions (For Windows Systems)
- After cloning the repository, create a virtual environment, which will store dependencies locally within the root directory of the project: 

      python -m venv venv

- Run this command to activate the virtual environment (run this command every time before starting the project): 

      venv\Scripts\activate

- Install the necessary dependencies with this command (the requirements.txt file is somewhat equivalent to package.json, which lists the dependencies):

      pip install -r requirements.txt

- Run this command to install Rasa in your project (uv will install faster): 

      uv pip install rasa-pro --extra-index-url=https://europe-west3-python.pkg.dev/rasa-releases/rasa-pro-python/simple/

- You also need to obtain a license key from Rasa (link if you don't have one yet: https://rasa.com/rasa-pro-developer-edition-license-key-request/), and run the following commands separately to set it as an environment variable:

      $env: RASA_PRO_LICENSE=<your-license-string>
      [System.Environment]::SetEnvironmentVariable('RASA_PRO_LICENSE','<your-license-string>','USER')

- You would also need an OpenAI API Key, and set that as an environment variable as well by running this command: 
      
      setx OPENAI_API_KEY your-api-key

### Instructions (For MacOS Systems)
- After cloning the repository, create a virtual environment, which will store dependencies locally within the root directory of the project: 

      python -m venv venv

- Run this command to activate the virtual environment (run this command every time before starting the project): 

      source venv/bin/activate

- Before installing dependencies, if you are on a non-Windows system, go to the requirements.txt file, and find and remove this line within the file: "pywin32==306"

- Install the necessary dependencies with this command (the requirements.txt file is somewhat equivalent to package.json, which lists the dependencies):

      pip install -r requirements.txt

- Run this command to install Rasa in your project (uv installs faster): 

      uv pip install rasa-pro --extra-index-url=https://europe-west3-python.pkg.dev/rasa-releases/rasa-pro-python/simple/

- You also need to obtain a license key from Rasa (link if you don't have one yet: https://rasa.com/rasa-pro-developer-edition-license-key-request/), and run the following commands separately to set it as an environment variable:

      export RASA_PRO_LICENSE="<your-license-string>"
      echo 'export RASA_PRO_LICENSE="<your-license-string>"' >> ~/.zshrc
      source ~/.zshrc

- You would also need an OpenAI API Key, and set that as an environment variable as well by running this command: 
      
      export OPENAI_API_KEY="your-api-key"
      echo 'export OPENAI_API_KEY="your-api-key"' >> ~/.zshrc
      source ~/.zshrc

### List of Commands
- When starting the Rasa project on your machine, start three different instances of your terminal, all of which have activated the virtual environment, (within the root directory of the project), and run the first three sets of commands in each of the three terminals.

- To run the flask server (required as it serves as an intermediary between front end and Rasa), run: 
      
      python main.py

- To run the Rasa server (required as it returns the answers to prompts), run: 

      cd rasa-calm
      rasa run

- To run Rasa actions (required as we are working with custom actions), run:
      
      cd rasa-calm
      rasa run actions

- To train the Rasa CALM Model (which must be done after first cloning this repository and every time a YAML file is modified), run this command:

      cd rasa-calm
      rasa train

- To run interact with Rasa chatbot in terminal (not required as it is for testing basic functionality of chatbot), run: 
      
      cd rasa-calm
      rasa shell

### Pyenv installation guide
- Run this command to install pyenv (ensure that your virtual environment is not created when doing these steps):

      pip install pyenv

- Run this command to install a specific version of python with pyenv:

      pyenv install 3.10.15

- Run this command to switch global python version with pyenv:

      pyenv global 3.10.15

- Then, in your project directory, run this command to ensure that the correct python version is running:

      python --version

- If this correct python version is shown after running the command above, then you can proceed with the other steps!

### Unique Cases
Sometimes you may encounter errors indicating that some packages are being installed using the legacy setup.py install. In that case install wheel (pip install wheel)

### Questions
- If you have any questions or concerns, please reach out to me, rohit, on the discord server.

