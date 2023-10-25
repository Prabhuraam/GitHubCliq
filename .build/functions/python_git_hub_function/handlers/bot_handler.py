import json
from handlers.GitHubConstants import GitHubConstants
import handlers.command_handler
from zcatalyst_cliq.bot_handler import (
    welcome_handler,
    message_handler,
    context_handler,
    mention_handler,
    menu_action_handler,
    webhook_handler,
    participation_handler,
    BotWelcomeHandlerRequest,
    BotMessageHandlerRequest,
    BotContextHandlerRequest,
    BotMentionHandlerRequest,
    BotMenuActionHandlerRequest,
    BotParticipationHandlerRequest,
    BotWebHookHandlerRequest,
    HandlerResponse
)
from zcatalyst_sdk.catalyst_app import CatalystApp
import logging

@welcome_handler
def welcome_handler_fn(req: BotWelcomeHandlerRequest, res: HandlerResponse, *args):
    res.text = f'hello {req.user.first_name}. Thank you for subscribing :smile:'
    return res


@message_handler
def msg_handler(req: BotMessageHandlerRequest, res: HandlerResponse, *args):
    
        print(req.message)
        msg = req.message
        text = ''
        if not msg:
            text = 'Please enable \'Message\' in bot settings'
        elif msg == "webhooktoken":
            Message = res.new_message() 
            Message.text = "Click on the token generation button below!"
            btnobj = res.new_button()
            btnobj.type = "+"
            action = btnobj.new_action_object()
            action.type = "invoke.function"
            conform = action.new_confirm_object()
            conform.title = "Generate Webhooks for a GitLab Project"
            conform.description = "Connect to GitLab Projects from within Cliq"
            conform.input  = "user_webhook_token"
            Actdata = action.new_action_data_obj()
            Actdata.name = "authenticate"
            action.data = Actdata
            action.confirm = conform
            btnobj.action = action
            btnobj.label = "Create Webhook"
            res.add_button(btnobj)
        else:
            text = "Oops! Sorry, I'm not programmed yet to do this :sad:"
        res.set_text(text)
        logging.info(res)
        return res
    
    
@context_handler
def ctx_handler(req: BotContextHandlerRequest, res: HandlerResponse, *args):
    app: CatalystApp = args[0]
    if req.context_id == 'personal_details':
        answer = req.answers
        name = answer.name.text
        dept = answer.dept.text

        text = f'Nice! I have collected your info: \n*Name*: {name} \n*Department*: {dept}'

        if answer.cache.text == 'YES':
            try:
                default_segment = app.cache().segment()
                default_segment.put('Name', name)
                default_segment.put('Department', dept)
                text += '\nThis data is now available in Catalyst Cache\'s default segment.'
            except Exception as e:
                logging.error(e)
        res.set_text(text)
    return res


@mention_handler
def mention_handler(req: BotMentionHandlerRequest, res: HandlerResponse, *args):
    text = f"Hey *{req.user.first_name}*, thanks for mentioning me here. I'm from Catalyst city"
    res.set_text(text)
    return res


@menu_action_handler
def action(req: BotMenuActionHandlerRequest, res: HandlerResponse, *args):
    text = ''
    res.bot = res.new_bot_details(GitHubConstants.BOT_NAME,text)
    if req.action_name == "Repos":
        reposArray = handlers.command_handler.getRepos()
        if len(reposArray) == 0:
            text = "There aren't are repos created yet."
        else:
             Slide = res.new_slide()
             text = "Here's a list of the *repositories*"
             Slide.type = 'table'
             Slide.title = "Repo details"
             headers = []
             headers.append('Name')
             headers.append('Private')
             headers.append('Open Issues')
             headers.append('Link')
             data = {
                 'headers':headers
             }
             rows = []
             for repo in reposArray:
                row = {
                    "Name": repo.get("name"),
                    "Private": "Yes" if repo.get("private") else "No",
                    "Open Issues": repo.get("open_issues_count"),
                    "Link": f"[Click here]({repo.get('html_url')})"
                }
                rows.append(row)
             data['rows'] = rows
             json_data = json.dumps(data)
             Slide.data = json_data
             res.add_slides(Slide)
    else:
        text = 'Menu action triggered :fist:'

    res.set_text(text)
    return res


@participation_handler
def participation(req: BotParticipationHandlerRequest, res: HandlerResponse, *args):
    text = ''
    if req.operation == 'added':
        text = 'Hi. Thanks for adding me to the channel :smile:'
    elif req.operation == 'removed':
        text = 'Bye-Bye :bye-bye:'
    else:
        text = 'I\'m too a participant of this chat :wink:'

    res.set_text(text)
    return res

@webhook_handler
def webhook_fn(req: BotWebHookHandlerRequest, res: HandlerResponse, *args):
    req_body: dict = json.loads(req.body)
    commitJson = req_body["commits"][0]
    res.new_message("A commit has been pushed !")
    res.bot = res.new_bot_details(GitHubConstants.BOT_NAME)
    commitMessage = res.new_slide()
    commitMessage.type = "text"
    commitMessage.title = "Commit message"
    res.add_slides(commitMessage)
    details = res.new_slide()
    details.type = "label"
    details.title = "Details"
    dataArray = []
    commiter = {}
    commiter['Committer'] = commitJson["author"]["username"]
    dataArray.append(commiter)
    repoName = {}
    repoName['Repo Name'] = req_body["repository"]["name"]
    dataArray.append(repoName)
    timestamp = {}
    timestamp['Timestamp'] = commitJson["timestamp"]
    dataArray.append(timestamp)
    compare = {}
    compare["Compare"] = f"[Click here]({req_body['compare']})"
    dataArray.append(compare)

    details.data = json.dumps(dataArray)
    res.add_slides(details)
    return res