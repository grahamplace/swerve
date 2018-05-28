from flask import redirect

SWERVE_MAP = {
    'dwh': 'https://github.com/opendoor-labs/dwh',
    'metrics': 'https://github.com/opendoor-labs/metrics',
    'honeycomb': 'https://github.com/opendoor-labs/honeycomb',
    'inbox': 'https://inbox.google.com/u/0/',
    'inbox-personal': 'https://inbox.google.com/u/1/',
    'cal': 'https://calendar.google.com/calendar/r',
    'jira': 'https://opendoor.atlassian.net/secure/RapidBoard.jspa?rapidView=25&projectKey=AXI',
    'bugs': 'https://opendoor.atlassian.net/projects/ENGBUGS/queues/custom/127',
}

def swerve(url_key):
    redirect_url = SWERVE_MAP.get(url_key, '/')
    return redirect(redirect_url, code=302)
