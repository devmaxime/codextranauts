import requests


def fetch_script_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        script_text = response.text
        return script_text
    else:
        print(f"Failed to download script. Status code: {response.status_code}")
        return None
