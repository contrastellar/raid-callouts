# How to contribute!
Hello! I'm glad you're reading this because hopefully it means you're going to help us create a better discord bot!

This is primarily open-source so that others can implement the code that we've written for their own use cases!

## Testing
Currently, we use GitHub actions to test the database portion of the codebase. It's a bit harder to test the Discord-centric commands otherwise.

## Submitting changes
Please send a [new GitHub Pull Request](https://github.com/contrastellar/raid-callouts/compare) with a clear list of what's been done!
When you send in a Pull Request (PR), we'll be super happy if you've made tests or otherwise commented your code clearly with what it does, and what libraries it uses in addition to our base libraries!

Please always write a clear commit message for your commits. One-line messages are fine for smaller changes, but bigger changes should be more details!

## Coding conventions
* Please take a look at our code base either on main or in the dev-branches! Once you get an idea of how we do things (generally [PEP 8](https://peps.python.org/pep-0008/)), but please feel free to fork + make any changes that fit in with our coding practices!
* There is a pretty big discrepency between the *goal* of hitting PEP 8 standards, and what we have going on, so style changes are also welcome!
* We prefer you to use `conda` for your environment management, but `pip` files for *most* things are included if you prefer! If you make edits to the base `conda` environment, please update the `environment.yml` and `requirements.txt` files accordingly!
* This is open source software, please consider writing code that is readable to people other than yourself!

## Issues and discussions on issues/PRs
Please be civil! The core contributers (contrastellar, DatJoshLife) reserve the right to remove any comments deemed inapproriate.

## Wiki contributions
The wiki for this repo serves as the main source of information with regards to onboarding anyone wishing to contribute! Please take a look at our explanation of our Postgresql back-end when writing new queries!
Any major edits that need to be made, can be brought up in ths issues tab!
