from typing import List
import json
from handlers.GitHubConstants import GitHubConstants
import zcatalyst_cliq.command_handler as command
import requests
from zcatalyst_cliq.command_handler import (
    execution_handler,
    suggestion_handler,
    CommandHandlerRequest,
    CommandSuggestion,
    HandlerResponse
)

@execution_handler
def executor(req: CommandHandlerRequest, res: HandlerResponse, *args):
    text = ''
    res.bot = res.new_bot_details(GitHubConstants.BOT_NAME,img=text)
    cmd = req.name

    if cmd == 'commits':
        suggestions = req.selections
        if not suggestions:
            text = 'Please select a repo from the suggestions.'
        else:
            repoName = suggestions[0].title
            commitsArray = getCommits(repoName)
            if len(commitsArray) == 0:
                text = "There aren't any commits made yet."
            else:
                Slide = res.new_slide()
                text = f"Here's a list of the latest {GitHubConstants.PER_PAGE} commits made to the repository *{repoName}*."
                Slide.type = "table"
                Slide.title = "Commit details"
                headers = []
                headers.append('Date')
                headers.append('Commit message')
                headers.append('Committed by')
                headers.append('Link')
                data = {
                    'headers':headers
                }
                rows = []
                for obj in commitsArray:
                    commit = obj.get("commit")
                    author = commit.get("author")
                    row = {
                        "Date": author.get("date"),
                        "Commit message": commit.get("message"),
                        "Committed by": author.get("name"),
                        "Link": f"[Click here]({obj.get('html_url')})"
                    }
                    rows.append(row)
                data["rows"] = rows
                json_data = json.dumps(data)
                Slide.data = json_data
                res.add_slides(Slide)

    elif cmd == 'issues':
        suggestions = req.selections
        if not suggestions:
            text = 'Please select a repo from the suggestions.'
        else:
            repoName = suggestions[0].title
            IssuesArray = getIssues(repoName)
            if len(IssuesArray) == 0:
                text = "There aren't any issues made yet."
            else:
                Slide = res.new_slide()
                text = f"Here's a list of the latest {GitHubConstants.PER_PAGE} issues raised to the repository *{repoName}*."
                Slide.type = "table"
                Slide.title = "Issue details"
                headers = []
                headers.append('Created At')
                headers.append('Title')
                headers.append('Created By')
                headers.append('Link')
                data = {
                    'headers':headers
                }
                rows = []
                for issueObj in IssuesArray:
                     
                     row = {
                        "Created At": issueObj.get("created_at"),
                        "Title": issueObj.get("title"),
                        "Created By": issueObj.get("user").get("login"),
                        "Link": f"[Click here]({issueObj.get('html_url')})"
                    }
                    
                rows.append(row)
                data["rows"] = rows
                json_data = json.dumps(data)
                Slide.data = json_data
                res.add_slides(Slide)

    else:
        text = "Slash command executed"

    res.text = text
    return res

def getCommits(name):
    req = f"https://api.github.com/repos/{getUsername()}/{name}/commits?per_page={GitHubConstants.PER_PAGE}"
    headers = {}
    headers['Authorization'] = f'Token {GitHubConstants.PERSONAL_ACCESS_TOKEN}'
    response = requests.get(url=req,headers=headers)
    data = response.json()
    if response.status_code == 200:
        return data    
        
    else:
        return []
        


def getUsername():
    req = "https://api.github.com/user"
    headers = {}
    headers['Authorization'] = f'Token {GitHubConstants.PERSONAL_ACCESS_TOKEN}'
    response = requests.get(url=req,headers=headers)
    data  = response.json()
    return data["login"]

def getRepos():
    req = "https://api.github.com/user/repos"
    headers = {}
    headers['Authorization'] = f'Token {GitHubConstants.PERSONAL_ACCESS_TOKEN}'
    response = requests.get(url=req,headers=headers)
    data = response.json()
    return data

def getIssues(repoName):
    req = f"https://api.github.com/repos/{getUsername()}/{repoName}/issues?per_page={GitHubConstants.PER_PAGE}"
    headers = {}
    headers['Authorization'] = f'Token {GitHubConstants.PERSONAL_ACCESS_TOKEN}'
    response = requests.get(url=req,headers=headers)
    data = response.json()
    return (data)

@suggestion_handler
def suggester(req: CommandHandlerRequest, res: List[CommandSuggestion], *args):
    suggestionList = []
    reposArray = getRepos()
    repos = reposArray
    repoNames = []
    for repo in repos:
        name = repo["name"]
        repoNames.append(name)
    if req.name == "commits" or req.name == "issues":
        for name in repoNames:
            sugg= CommandSuggestion(title=name)
            suggestionList.append(sugg)
    return suggestionList
