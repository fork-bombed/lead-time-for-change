# Installation

Clone this repository
```bash
git clone https://github.com/fork-bombed/lead-time-for-change lead_time_for_change
```

Once cloned, copy the `ltfc` folder to the root directory of your folder (named `my_repo` in this example)
```bash
cp -r lead_time_for_change/ltfc my_repo/
```

To get it to run automatically, you will need to install the GitHub action script included in the `ltfc` folder. To do this you'll need to create a `.github/workflows` folder in the root directory of your repository. You can skip this if you already have a workflows folder.

```bash
cd my_repo
mkdir .github .github/workflows
```

To install the script you'll need to move the `release.yml` file into the `.github/workflows` directory.

```bash
mv ltfc/release.yml .github/workflows 
```

# Customisation

The release template is completely customisable. You can find the markdown template in `ltfc/templates/default.md`. You can use the variable names provided in markdown e.g `{version}` which will be replaced using format strings in the `github_api.py` file. If you wish to change the variables being passed in, you will need to change the code in that file to include your new variables.

If you want to import any more packages you will need to include them in the `ltfc/requirements.txt` file. This tells the GitHub Actions runner what to install in the virtual python environment, so make sure all your dependencies are in it or the runner will fail.