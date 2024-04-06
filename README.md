# PyShiny Express: Shiny Weather App

## Module 05 - Instruction - Adrian Vega

## Prerequisites
Before you start, have the following installed:

* Python: Install the most recent version from python.org.
* Git: Download and install Git from git-scm.com.
* Visual Studio Code (VS Code): Download from code.visualstudio.com.
* VS Code Extensions: Install the Python extension and the Shiny extension in VS Code.

### Configurations
* Configure Git: Set up your user name and email with Git using the following commands in your terminal. Change the values to your name and email address. This is a one-time setup.

        git config --global user.name "Your Name"
        git config --global user.email "youremail@example.com"

## Set up the Project
### Commands
Commands are operating system-specific. These commands are for Windows users. On Mac/Linux, generally use python3 instead of py. Edit your README.md to reflect the commands that work on your machine.

### Verify Installations
1. Open project folder in VS Code.
2. Open a new terminal - on Windows, ensure the terminal type is PowerShell (not the old cmd)
3. Run the following commands in the terminal one at a time to verify installations.

        py --version
        git --version
        git config user.name
        git config user.email

## Python Project Virtual Environment
Run the following commands in the terminal to set up a project virtual environment and install the necessary packages. Run them from the root project folder. Use PowerShell on Windows or the terminal on macOS and Linux.

### Create a Project Virtual Environment (generally one-time setup)
Create a project virtual environment in the .venv folder of the project root directory.

        py -m venv .venv
Creating a project virtual environment is generally a one-time setup. Once the folder exists, we can activate it to work on the project.

If VS Code pops up and says: We noticed a new environment has been created. Do you want to select it for the workspace folder? select Yes.

### Activate the Project Virtual Environment (when you work on the project)
Once the project virtual environment exists, we activate the virtual environment to work on the project - or when we open a new terminal.

On Windows:

        .venv\Scripts\Activate
On macOS and Linux:

        source .venv/bin/activate
Verify: Generally when the environment is active, (.venv) will appear in the terminal prompt.

We also need to select this project virtual environment in VS Code. To do this:

1. Open the VS Code command palette (Ctrl+Shift+P).
2. Search for "Python: Select Interpreter".
3. Select the .venv folder in the project root directory.

### Install Packages into the Active Project Virtual Environment
When the project virtual environment is active, install packages into the project virtual environment so they are available for use in the Python code.

NOTE:

* We install packages into the project virtual environment.
* We import packages into Python code (after they have been installed).

First, upgrade pip and setuptools (core packages) for good measure. NOTE: Using the palmerpenguins package requires setuptools. Then, install the project-specific required packages.

With the project virtual environment active in the terminal, run the following commands:

        py -m pip install --upgrade pip setuptools
        py -m pip install --upgrade -r requirements.txt

Installing packages is generally a one-time setup.

## Run the App
With your project virtual environment active in the terminal and the necessary packages installed, run the app with live reloading and automatically open it in the browser:

        shiny run --reload --launch-browser penguins/app.py

While the app is running, that terminal is fully occupied. Open a new terminal to run other commands.

## Build the App to Docs Folder and Test Locally
With your project virtual environment active in the terminal and the necessary packages installed, remove any existing assets and use shinylive export to build the app in the dashboard folder to the docs folder:

        shiny static-assets remove
        shinylive export dashboard docs

Optional: Edit docs/index.html to show a custom tab title and add a favicon.

        <title>PyShiny Dashboard</title>
        <link rel="icon" type="image/x-icon" href="./favicon.ico">

After the app is built, serve the app locally from the docs folder to test before publishing to GitHub Pages. In the terminal, run the following command from the root of the project folder:

        py -m http.server --directory docs --bind localhost 8008

Open a browser (tested with Chrome) and navigate to http://localhost:8008 to view the app running locally.

## After Editing, Git Add/Commit/Push Changes to GitHub
After editing project files, use Git add/commit/push changes to the main branch of the repository. Note that if a terminal is serving an app, it is not available for other commands. Run the following commands from a new or available terminal to git add/commit/push changes to GitHub. Replace "Your commit message" with a meaningful message about the changes you made to the project files. Run commands one at a time and wait for each to complete before running the next.

        git add .
        git commit -m "Your commit message"
        git push -u origin main

## Publish the App with GitHub Pages (one-time setup)

The first time you set up an app, you'll need to navigate to the repository on GitHub and configure the settings to publish the app with GitHub Pages. After configuring the repository once, each time you push changes to the main branch, the app will automatically update.

1. Go to the repository on GitHub and navigate to the Settings tab.
2. Scroll down and click the Pages section.
3. Select branch main as the source for the site.
4. Change from the root folder to the docs folder to publish from.
5. Click Save and wait for the site to build.
6. Edit the "About" section of the repository to include a link to the live app.

## Resources

The Shiny development team. Shiny for Python [Computer software]. https://github.com/posit-dev/py-shiny