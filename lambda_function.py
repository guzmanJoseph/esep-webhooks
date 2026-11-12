import json
import os
import urllib.request

def lambda_handler(event, context):
    if isinstance(event, str):
        event = json.loads(event)

    if isinstance(event, dict) and isinstance(event.get("body"), str):
        try:
            event = json.loads(event["body"])
        except json.JSONDecodeError:
            pass

    issue = event.get("issue") if isinstance(event, dict) else None
    if not isinstance(issue, dict) or not issue.get("html_url"):
        return {"statusCode": 200, "body": "Ignored event"}

    payload = json.dumps({
        "text": f"Issue Created: {issue['html_url']}"
    }).encode("utf-8")

    request = urllib.request.Request(
        os.environ["SLACK_URL"],
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=8) as response:
        return {"statusCode": 200, "body": response.read().decode("utf-8")}
