# Github API (no authentication)

import csv
import requests


def main():
    repos = ['Zelig', 'ZeligChoice', 'ZeligGAM', 'ZeligEI', 'ZeligMultilevel',
             'WhatIf', 'Amelia', 'ei', 'RobustSE', 'IQSSdevtools', 'zeligverse',
             'zelig-demos', 'zeligproject.org']

    issues = []
    for repo in repos:
        repo_issues = get_issues('IQSS', repo)
        issues = [*issues, *repo_issues]

    fieldnames = ['repository', 'milestone', 'number', 'title', 'state',
                  'assignee', 'created_at', 'closed_at', 'created_by',
                  'author_association']
    with open("issues.csv", "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        for issue in issues:
            writer.writerow(issue)


def get_issues(username, repository):
    """Returns the results of an http GET request to the Github API. Accepts
    strings for username and repository and returns a tuple with the repository
    name and the list of issues."""

    host = 'https://api.github.com/repos/'
    url = host + username + '/' + repository + '/issues'

    issues = []
    response = requests.get(url)
    print("API response: " + str(response))

    data = response.json()

    fields = ['number', 'title', 'state', 'created_at', 'closed_at',
              'author_association']

    for dict_i in data:
        tmp = {field: dict_i[field] for field in fields if field in dict_i}
        tmp['created_by'] = dict_i['user']['login']
        if dict_i['milestone'] is None:
            tmp['milestone'] = 'None'
        else:
            tmp['milestone'] = dict_i['milestone']['title']
        if dict_i['assignee'] is None:
            tmp['assignee'] = 'None'
        else:
            tmp['assignee'] = dict_i['assignee']['login']
        tmp['repository'] = repository
        issues.append(tmp)

    print(str(len(issues)) + " issues from repository " + repository + ".")
    return issues


if __name__ == '__main__':
    main()
