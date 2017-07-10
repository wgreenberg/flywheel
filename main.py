from lib import summarizer

from web_app import app

# server stuff goes here
app.run(debug=True)

print(summarizer.summarize('hello world'))
