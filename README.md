# raid-callouts


# Info


# Runtime 


# Installation & Testing

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
- Unsure of what else needs to be done, all requirements that I can think of have been fulfilled.

# Contributing

Pull requests are welcome. For major changes, please open issues first to discuss what you would like to change.

# License

The license for `raid-callouts` is the `GNU General Public License`. Please see [License](https://github.com/contrastellar/OpossumBot_v3/blob/main/LICENSE) for more information.

