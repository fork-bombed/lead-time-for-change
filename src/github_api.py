import github
from datetime import datetime, timedelta

def get_client() -> github.Github:
    # temporarily store token in file
    with open('token') as f:
        token = f.read()
    return github.Github(token)


def get_last_modified_date(last_modified: str) -> datetime:
    # in format `Wed, 18 Nov 2020 10:24:29 GMT`
    return datetime.strptime(last_modified,'%a, %d %b %Y %H:%M:%S %Z')


def get_release_template(release: github.GitRelease.GitRelease, repo: github.Repository.Repository) -> str:
    with open('template.md') as f:
        template = f.read()
    return template.format(
        version     = release.tag_name,
        lead_time   = get_lead_time_for_change(release, repo)
        )


def get_commit_date(commit: github.Commit.Commit) -> datetime:
    return commit.commit.author.date


def get_lead_time_for_change(release: github.GitRelease.GitRelease, repo: github.Repository.Repository) -> timedelta:
    previous = repo.get_releases()[1]
    created = previous.created_at
    commits = [datetime.timestamp(get_commit_date(x))-datetime.timestamp(created) for x in repo.get_commits() if get_commit_date(x) >= created]
    return timedelta(seconds=sum(commits)/len(commits))


def main():
    client = get_client()
    # will need to be passed in, can hardcode for testing
    repo = client.get_user().get_repo('resgroup-prototype')
    release = repo.get_latest_release()
    release.update_release(name=release.title, message=get_release_template(release, repo))


if __name__ == '__main__':
    main()
