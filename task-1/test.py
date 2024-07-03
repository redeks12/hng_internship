from requests import get

request = get(
    "https://nandom.pythonanywhere.com/api/hello?visitor_name=nandom",
    headers={"X-Forwarded-For": "102.88.36.38"},
)

print(request.json(), request.headers)
