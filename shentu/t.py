import requests


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Referer": "http://47.99.111.192/httpbin/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ik9HVTVNakE1T0RZdFpEQXoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhbnlvbmciLCJzdWIiOiJ1c2VyLTEyMyIsIlVzZXJJZCI6InVzZXItMTIzIiwiVXNlclJvbGUiOjEsIk5TIjoidGVzdCIsImlhdCI6MTc1OTUxMzI3MiwiZXhwIjoxNzU5NTk5NjcyLCJuYmYiOjE3NTk1MTMyNzJ9.NlVw9Paknz8xowTNWtc29WKkrobzDk5e5ZY8tDpltiAPxyyZrd0KOX_2DQU73sKdIt5DUvDr-qCsPkCxASwGbpmyrB62VO_kSpSYgRlGAf-ppnRKCY1UV3uWr8Nn7SqDLQUqFiQDXGL_kYnaEyacIqa8g6UHLKtofA1sktA0w2jF2lHuXrRi3k8O0jThsinCNn_tVgtb3-IOjbgjhiwQbR0bRu6pqTWeDayEAXSjl-jbLaPlZjr79p_6cBjHEJNjDa19FfwlxX3OG0m6EDZCmFkNBlbfokKUJqH2iPayzINmiFAYuya2PL9ezeldYd_EWwI6fKF2q5cDPmB2nl8cOQ",
}
url = "http://47.99.111.192/httpbin/headers"
response = requests.get(url, headers=headers, verify=False)

print(response.text)
print(response)