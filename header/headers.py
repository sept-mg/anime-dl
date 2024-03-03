import yaml
def getHeaders():
    with open("header/headers.yml") as headers:
        browser_headers = yaml.safe_load(headers)
    return browser_headers["Firefox"]