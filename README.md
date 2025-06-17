# Random Drankspel

This is the repository for the Random Drankspel generator. This application is designed to create a way to pick a random drinking game.

## Getting Started

This project is built using both [Django](https://github.com/django/django) for the backend and [VueJS](https://vuejs.org) for the frontend.

### Setup backend

0. Get at least [Python](https://www.python.org) 3.11 installed on your system.
1. Clone this repository.
2. If `pip3` is not installed on your system yet, execute `apt install python3-pip` on your system.
3. Also make sure `python3-dev` is installed on your system, execute `apt install python3-dev`.
4. Install Poetry by following the steps on [their website](https://python-poetry.org/docs/#installation). Make sure poetry is added to `PATH` before continuing.
5. Make sure `poetry` uses your python 3 installation: `poetry env use python3`.
6. Go to the `backend` directory.
7. Run `poetry install` to install all dependencies.
8. Run `poetry shell` to start a shell with the dependencies loaded. This command needs to be ran every time you open a new shell and want to run the development server.
9. Run `cd website` to change directories to the `website` folder containing the project.
10. Run `./manage.py migrate` to initialise the database and run all migrations.
11. Run `./manage.py createsuperuser` to create an administrator that is able to access the backend interface later on. The password you set here will not be used as the openid server will be used for identification, be sure to set the super user to your science login name.
12. Run `./manage.py runserver` to start the development server locally.

Now your server is setup and running on `localhost:8000`. The administrator interface can be accessed by going to `localhost:8000/admin`.

### Setup frontend

1. Install the [Yarn](https://yarnpkg.com/) package manager
2. Clone this repository
3. Go to the `frontend`.
4. Use `yarn install` to install the required packages
5. Use `yarn serve` to serve the test server
6. Note that you might need to setup a `.env` file in the root of the cloned repository. The `.env` file will need to look something like the following (for local development):

```
VUE_APP_BACKEND_URI=http://localhost:8000/api/v1
```

## Docker container

A `Dockerfile` is included in the respective folders of both the `backend` and `frontend` of the repository. For building the docker file, you can run `docker build -t [tag] .` in the respecitve folder of the docker you want to build. An example docker-compose file is added as ```docker-compose.yml.example```. Note that for running this docker-compose file, the `setup.sql` in `backend/database_init` should be configured as well. 

### Setting environment variables for the frontend

Normally, environment variables are included during build and can not be changed afterwards. This is a problem when building a docker container which can be applied to different scenarios (e.g. with different API servers). Due to this fact, environment variables can be either included during build with a `.env` file in the root directory or with docker environment variables afterwards. Using docker environment variables will overwrite the environment variables included during build.

Environment variables that are available and should be overwritable by docker environment variables later should be included in the `docker.blueprint.env` file. Note that this file must use `'` for indicating strings and the format is as follows:
```
    '[NAME_OF_VARIABLE_IN_VUE]': '${NAME_OF_ENV_VARIABLE}'
```
Before starting the `nginx` process, the docker environment variables will be set under the `window.__env__` variable in the `index.html` file.

### Using environment variables for the frontend

To use environment variables that can be set during runtime (with docker environment variables), add the variable to the `docker.blueprint.env` file as explained above. Then use the `getEnvVar` function in `src/util/env.ts` for getting the value of an environment variable. This function will first check wether it is set in the `window.__env__` variable and will then look if it is an environment variable.

## Voice assistants

The backend of this project supports the uses of Voice assistants to interact with the drinking games registered. Look at the method below to find out how to use them on your platform.

### Siri

Siri natively support [shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios). It is very easy to interact with this project via Siri. Setup a shortcut in the Shortcuts app on iOS. Alternatively, you can use this [link](https://www.icloud.com/shortcuts/3e0d01e6408140cdb41a895e4c752823) to import a Dutch version of the shortcut (change the trigger to English for an English version).

### Google Assistant

The Google Assistant side of this project is more complex, as Google has more features for adding Voice assistants to its own Google Assistant. We will be using [Dialogflow](https://dialogflow.cloud.google.com) for interacting with our voice assistant. The steps how to set this up are displayed below:

1. Setup a voice assistant on Google's [Dialogflow platform](https://dialogflow.cloud.google.com).
2. Make sure to setup a [service account](https://cloud.google.com/docs/authentication/getting-started ) for the Dialogflow project such that our application can interact with it later.
3. Download the JSON key file and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable (either in the `docker-compose.yml` file or on your own machine) to the absolute path to the credentials file.
4. Set the `GOOGLE_AGENT_NAME` environment variable to the name of the agent displayed in the Dialogflow console.
5. Set the `GOOGLE_INTENT_TRIGGER` environment variable to the trigger value (such as `Give a random drinking game`).
6. Set the `GOOGLE_INTENT_RESPONSE` environment variable to the response value (such as `Here is your drinking game: {}`). Note that the response will be formatted by Python, and using `{}` is obligatory (the random drinking game will be substituted with it).
7. Run the server.
8. Execute `manage.py reset_dialgflow_agent` to create the needed intent within Dialogflow.
9. Setup the fullfillment URL within the Fullfillment tab in the Dialogflow console. Make sure your URL ends in `/api/dialogflow` (the endpoint for dialogflow is located there).
10. You can now try out the Voice assistant in the Dialogflow console and add it to your phone.
