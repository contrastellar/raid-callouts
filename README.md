[![test and deploy](https://github.com/contrastellar/raid-callouts/actions/workflows/deploy.yaml/badge.svg)](https://github.com/contrastellar/raid-callouts/actions/workflows/deploy.yaml)

# Info
`raid-callouts` is a toolset developed for the purpose of keeping track of when people are going to be absent from raid nights for my FFXIV raid team. There's some back-end things that go unsaid in the code, but will be documented here.

# Runtime
Currently, this Discord bot is designed to run in two parts, which each part will be gone over here. There is also a "database helper" module, which is called as needed by the bot components.

On the server itself, the `bot_core` and the `bot_aux` are "composed" into two containers using Docker Compose on a service account, and then can be invoked or run using `cron` in order to schedule things like the daily "posting" of the next week's callouts.

## bot_core ("listener")
The bot's core, is an "always on" bot, that listens for slash commands to be sent to it, and responds as necessary. Commands and their outputs can be viewed on the [wiki found here](https://github.com/contrastellar/raid-callouts/wiki)

## bot_aux ("poster")
The bot's "auxillary" is a python script developed in order to post on script execution, a formatted Discord message that details the callouts for the next `7` days.

# Quickstart (/w conda)

## `conda` install

`conda` can be installed from [here](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html).

## Once `conda` is installed

1. Clone the repo

2. Navigate to the cloned repo
```sh
cd ./raid-callouts
```

3. Install the environment /w conda & pip
```sh
conda env create --file environment.yml
# Run this pip command to assure that all requirements are actually installed
pip install -r requirements.txt
```

4. Activate the environment
```sh
conda activate raid-callouts
```

5. `conda` handles all the installation of the packages and dependencies for these modules. A `requirements.txt` is maintained for both `virtualenv` users, and for GitHub Actions runtime simplicity.

6. You need to provide your own `database.ini` file, that contains your own PSQL database, if you wish to self-host the bot. Otherwise, testing will be done on Pull Request.

# TODO

- All major milestones have been reached or are in PRs.

# Contributing

Pull requests are welcome. For major changes, please open issues first to discuss what you would like to change.

# License

The license for `raid-callouts` is the `GNU General Public License`. Please see [License](https://github.com/contrastellar/OpossumBot_v3/blob/main/LICENSE) for more information.

