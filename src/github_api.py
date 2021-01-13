from datetime import datetime, timedelta
import github
import release
import repository
import commit


def get_lead_time(release: release.Release, repository: repository.Repository) -> timedelta:
    # TODO: Lead-time doesn't work.
    previous_release = repository.get_releases()[1]
    previous_created = datetime.strptime(previous_release["created_at"], "%Y-%m-%dT%XZ")

    commits = [
        datetime.timestamp(commit.get_date()) - datetime.timestamp(previous_created)
        for commit in repository.get_commits() if commit.get_date() >= previous_created
    ]

    return timedelta(seconds=sum(commits)/len(commits))


def get_release_template(release: release.Release, repo: repository.Repository) -> str:
    with open("template.md") as file:
        template = file.read()

    return template.format(
        version=release.get_tag_name(),
        lead_time=get_lead_time(release, repo)
    )


if __name__ == "__main__":
    with open("token") as file:
        token = file.read()

    client = github.Github(token)
    repository = client.get_repository("resgroup-prototype")
    release = repository.get_latest_release()
    release.update(
        message=get_release_template(
            release=release, repo=repository
        )
    )
