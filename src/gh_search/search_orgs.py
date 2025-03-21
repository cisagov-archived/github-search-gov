#!/usr/bin/env python3 -u
"""Search government GitHub organizations for usage of actions.

BeautifulSoup-based code is fragile and may break if GitHub's HTML changes
"""

# Standard Python Libraries
import logging
import os

# Third-Party Libraries
from bs4 import BeautifulSoup
from github import Github
import requests

# CONSTANTS
ACTION_OF_INTEREST = "tj-actions/changed-files"
GOV_COMMUNITY_URL = "https://government.github.com/community/"
GROUP_PREFIX = "governments-us"


def main():
    """Search government GitHub organizations for usage of actions."""
    logging.basicConfig(level=logging.INFO)

    # Get the token from the environment variable
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        logging.error("GITHUB_TOKEN environment variable not set.")
        exit(1)

    # Initialize the GitHub client with the token
    gh_client = Github(token)

    try:
        # Fetch the webpage
        response = requests.get(GOV_COMMUNITY_URL, timeout=60)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error("Error fetching the community page: %s", e)
        exit(1)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # First, get all the h3 elements with the specific classes.
    org_groups = soup.find_all(
        "h3", class_="alt-h3 mb-3", id=lambda x: x and x.startswith(GROUP_PREFIX)
    )

    print(f"# Searching for {ACTION_OF_INTEREST} in {len(org_groups)} groups")

    # Iterate over each group of organizations
    for group in org_groups:
        print(f"# {group['id']}")
        # Get all the links in the group
        links = group.find_next_sibling("div", class_="orgs").find_all("a")
        for link in links:
            org_name = link["title"].strip()
            print(f"# {org_name}")

            search_query = (
                f"org:{org_name} uses: {ACTION_OF_INTEREST} language:YAML path:.github/"
            )
            try:
                code_results = gh_client.search_code(query=search_query)
            except Exception as e:
                logging.error("Error searching for %s: %s", org_name, e)
                continue
            print(f"# Found {code_results.totalCount} results for {org_name}")
            for code in code_results:
                print(f"{code.html_url}")


if __name__ == "__main__":
    main()
