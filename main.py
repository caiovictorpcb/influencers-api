from flask import Flask, render_template, request
import requests


app = Flask(__name__)


def scrap_data(username: str, token: str):
    print(f"Fetching data for {username}...")
    #print(f"Token: {token}")
    url = f'https://graphql.inbeat.co/engagement-calculator'
    response = requests.post(url, json={'platform': 'instagram',
                                        'username': username,
                                        'token': token},
                             headers={'Content-Type': 'application/json',
                                      'Referer': 'https://www.inbeat.co/',
                                      'Origin': 'https://www.inbeat.co',
                                      'Connection': 'keep-alive'})
    print(f'response {response}')
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")
    data = response.json()
    return data


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        username = request.form['username']
        token = request.form['token']
        data = scrap_data(username, token)
        return render_template('result.html', data=data)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)