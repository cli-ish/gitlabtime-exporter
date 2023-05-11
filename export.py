import argparse
import csv
import datetime
import json
import time
from datetime import datetime as datetime_format

import requests


def get_graphql_response(url, token, query):
    data = requests.post(url, json=query, headers={"Authorization": "Bearer " + token})
    return data.content.decode()


def get_issue_spend_times(gitlab_url, bearer_token, project_name):
    ql_query = """
query getProject($path: ID!, $afterCursor: String, $pageSize: Int) {
  project(fullPath: $path) {
    issues(first: $pageSize, after: $afterCursor) {
      edges {
        node {
          iid
          title
          timelogs {
            edges {
              node {
                spentAt
                user { name }
                summary
                timeSpent
              }
            }
            totalSpentTime
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
    """

    issues_found = []
    after = ""
    while True:
        result2 = get_graphql_response(gitlab_url + "/api/graphql", bearer_token, {
            "operationName": "getProject",
            "query": ql_query,
            "variables": {
                "pageSize": 100,
                "path": project_name,
                "afterCursor": after
            }
        })
        result = json.loads(result2)

        issue_times = result["data"]["project"]["issues"]
        for issueNode in issue_times["edges"]:
            node = issueNode["node"]
            for time_node in node["timelogs"]["edges"]:
                new_issue = {
                    "project": project_name,
                    "iid": node["iid"],
                    "title": node["title"],
                    "date": time_node["node"]["spentAt"],
                    "user": time_node["node"]["user"]["name"],
                    "summary": time_node["node"]["summary"],
                    "spend": time_node["node"]["timeSpent"],
                }
                issues_found.append(new_issue)

        if issue_times["pageInfo"]["hasNextPage"]:
            after = issue_times["pageInfo"]["endCursor"]
        else:
            break
    return issues_found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gitlab-instance', dest='gitlab', type=str, help='url of gitlab (https://yourgitlab.com)')
    parser.add_argument('--project-names', dest='projects', type=str, help='project path (group/project)')
    parser.add_argument('--access-token', dest='access_token', type=str,
                        help='user access token (xxxxx-XxXxXxXxXxXxXxXxXxXx)')
    args = parser.parse_args()

    projects = args.projects.split(",")
    issues = []
    for project in projects:
        issues += get_issue_spend_times(args.gitlab, args.access_token, project)
    filename = 'timesheet_' + time.strftime("%Y-%m-%d") + '.csv'

    utcdiff = datetime_format.now() - datetime_format.utcnow()
    # newline='' added because windows added 2 newlines for each newline?
    with open(filename, 'w', newline='', encoding="utf8") as file:
        w = csv.writer(file)
        w.writerow(["Spend At", "Spend At Clock", "Project", "Issue Id", "Title", "Time Spend", "User", "Summary"])
        f = "%Y-%m-%dT%H:%M:%SZ"
        for issue in issues:
            out = datetime_format.strptime(issue["date"], f) + utcdiff
            w.writerow(
                [
                    out.strftime("%d.%m.%Y"),
                    out.strftime("%H:%M:%S"),
                    issue["project"],
                    "#" + issue["iid"],
                    issue["title"],
                    str(datetime.timedelta(seconds=issue["spend"])),
                    issue["user"],
                    issue["summary"]
                ])


if __name__ == "__main__":
    main()
