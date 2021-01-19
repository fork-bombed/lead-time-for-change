<<<<<<< HEAD
from datetime import datetime, timedelta
import commit
import github
import release
import repository
import yaml, os, sys

CONFIG_NAME = "config.yaml"

def get_lead_time(release: release.Release, repository: repository.Repository) -> timedelta:
    # If there's only one release then get all the commits and compare 
    # to the creation of the repository.
    if len(repository.get_releases()) == 1:
        commits = [
            datetime.timestamp(commit.get_date()) - datetime.timestamp(repository.get_creation_time())
            for commit in repository.get_commits()
        ]
    else:
        previous_release = repository.get_releases()[1]
        previous_created = previous_release.get_creation_time()

        commits = [
            datetime.timestamp(commit.get_date()) - datetime.timestamp(previous_created)
            for commit in repository.get_commits() if commit.get_date() >= previous_created
        ]

    return timedelta(seconds=sum(commits)/len(commits))


def get_release_template(release: release.Release, repo: repository.Repository) -> str:
    with open("src/template.md") as file:
        template = file.read()

    return template.format(
        version=release.get_tag_name(),
        lead_time=get_lead_time(release, repo)
    )


if __name__ == "__main__":
    if not os.path.isfile(f'../{CONFIG_NAME}'):
        print(f'{CONFIG_NAME} not found')
    with open(f'../{CONFIG_NAME}') as file:
        CONFIG = yaml.safe_load(file)
    client = github.Github(CONFIG.get('token'))
    repository = client.get_repository(CONFIG.get('repo'))
    release = repository.get_latest_release()
    release.update(
        message=get_release_template(
            release=release, repo=repository
        )
    )
=======
from datetime import datetime, timedelta
import commit
import github
import release
import repository
import yaml, os, sys

CONFIG_NAME = "config.yaml"

def get_lead_time(release: release.Release, repository: repository.Repository) -> timedelta:
    # If there's only one release then get all the commits and compare 
    # to the creation of the repository.
    if len(repository.get_releases()) == 1:
        commits = [
            datetime.timestamp(commit.get_date()) - datetime.timestamp(repository.get_creation_time())
            for commit in repository.get_commits()
        ]
    else:
        previous_release = repository.get_releases()[1]
        previous_created = previous_release.get_creation_time()

        commits = [
            datetime.timestamp(commit.get_date()) - datetime.timestamp(previous_created)
            for commit in repository.get_commits() if commit.get_date() >= previous_created
        ]

    return timedelta(seconds=sum(commits)/len(commits))


def get_release_template(release: release.Release, repo: repository.Repository) -> str:
    with open("src/template.md") as file:
        template = file.read()

    return template.format(
        version=release.get_tag_name(),
        lead_time=get_lead_time(release, repo)
    )


if __name__ == "__main__":
    if not os.path.isfile(f'../{CONFIG_NAME}'):
        print(f'{CONFIG_NAME} not found')
    with open(f'../{CONFIG_NAME}') as file:
        CONFIG = yaml.safe_load(file)
    client = github.Github(CONFIG.get('token'))
    repository = client.get_repository(CONFIG.get('repo'))
    release = repository.get_latest_release()
    release.update(
        message=get_release_template(
            release=release, repo=repository
        )
    )
>>>>>>> 6da4b189469f674adb118660bf0e6f4c0f97ed33
