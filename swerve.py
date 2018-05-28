from flask import redirect

SWERVE_MAP = {
    'bugs': 'https://opendoor.atlassian.net/projects/ENGBUGS/queues/custom/127',
    'cal': 'https://calendar.google.com/calendar/r',
    'dwh': 'https://github.com/opendoor-labs/dwh',
    'honeycomb': 'https://github.com/opendoor-labs/honeycomb',
    'inbox-personal': 'https://inbox.google.com/u/1/',
    'inbox': 'https://inbox.google.com/u/0/',
    'jfrog': 'https://opendoor.jfrog.io/opendoor/webapp/#/profile',
    'jira': 'https://opendoor.atlassian.net/secure/RapidBoard.jspa?rapidView=25&projectKey=AXI',
    'metrics': 'https://github.com/opendoor-labs/metrics',
}

def swerve(url_key):
    redirect_url = SWERVE_MAP.get(url_key, '/')
    return redirect(redirect_url, code=302)
