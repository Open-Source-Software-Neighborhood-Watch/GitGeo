"""Functionality for scanning multiple repos."""

import time
import os

from gitgeo.custom_csv import create_csv, add_committer_to_csv
from gitgeo.geolocation import get_country_from_location
from gitgeo.github import get_contributors, get_contributor_location
from gitgeo.pypi import extract_github_owner_and_repo


def scan_multiple_repos(input_file="repos.txt", num=100, force=False, repo_cache="repos.json", contributor_cache="contributors.json"):
    """Create csv of data for multiple repos.

    Scan through repos provided in repos.txt and create a single csv that
    stores all contributor-related data for each contributor in each repo.

    Args:
        input_file - file containing repo list
        num - max number of contributors to analyze per repo
        force - force a reset of json cache files

    Returns:
        None
    """
    # create csv to store multi-repo scan results
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    create_csv("multirepo", timestamp)

    # clear cache if force
    if force and os.path.exists(repo_cache):
        os.remove(repo_cache)
    if force and os.path.exists(contributor_cache):
        os.remove(contributor_cache)

    # open file that contains repos to scan and append contributors for each
    # repo to csv. Also, repos.txt must contain repo names, one repo per line.
    with open(input_file, "r") as input_repos:
        for repo in input_repos:
            # Skip blank lines
            if repo == "":
                continue
            # strip blank space before extracting owner and repo name
            repo_ending_string = extract_github_owner_and_repo(repo.strip())
            contributors = get_contributors(repo_ending_string, repo_cache, num)

            for i, contributor in enumerate(contributors):
                if i >= num:
                    break
                location = get_contributor_location(contributor, contributor_cache)
                country = get_country_from_location(location)
                add_committer_to_csv(
                    "multirepo",
                    repo_ending_string,
                    timestamp,
                    contributor,
                    location,
                    country,
                )
