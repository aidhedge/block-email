from flask import Flask
from flask import render_template
from flask import request
import email_service
import json
import os

app = Flask(__name__,template_folder='templates')

@app.errorhandler(404)
def handle_404(err):
    return 'Aidhedge Send mail block'

@app.errorhandler(500)
def handle_500(err):
    import sys
    return json.dumps({'emailSent':False, 'error':sys.exc_info()[1]})

@app.route('/', methods=['GET'])
def index():
    return 'Aidhedge Send mail block'

@app.route('/', methods=['POST'])
def entry():
    try:
        recipient = request.form['recipient']
        subject = request.form['subject']
        data = request.form.get('data', None)
        template = request.form.get('template', 'no_template')
    except KeyError:
        return json.dumps({'status':'error', 'description':'Recipient and/or Subject is missing'})
    if data:
        try:
            data = json.loads(data)
        except BaseException:
            return json.dumps({'emailSent':False, 'error':'Malformed data json-string'})
    email = email_service.EmailHandler(to=recipient, subject=subject)
    content = render_template("{}.html".format(template), data=data)
    email.html = content
    res = email.send()
    return json.dumps(dict(success=True, payload=res))

if __name__ == "__main__":
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)