from flask import Flask, render_template, request, redirect, jsonify
from twilio.rest import Client
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant

app = Flask(__name__)
fake = Faker()

@app.route('/')
def load():
    print('App Running...')

    return render_template('index.html')

@app.route('/', methods=['post'])
def login():
    user = request.form['user_name']
    password = request.form['pass_word']
    phoneNo = request.form['phoneno']

    if user == 'admin' and password == 'aRyAn':
        ACCOUNT_SID = 'AC291104b9da0c838324afb38b6271fb9b'
        AUTH_TOKEN = 'bf1bf1377d6074af78d7304d7c9a34c1'
        Tclient = Client(ACCOUNT_SID, AUTH_TOKEN)
        verfication = Tclient.verify.services('VAc59c05709ed6664de8094e279a53fb1f').verifications.create(to=phoneNo, channel='sms')

        return render_template('otp.html')
    else :
        return render_template('user_error.html')

@app.route('/otp', methods=['post'])
def check():
    mobile_no = request.form['otp_phone']
    received = request.form['otp']
    ACCOUNT_SID = 'AC291104b9da0c838324afb38b6271fb9b'
    AUTH_TOKEN = 'bf1bf1377d6074af78d7304d7c9a34c1'
    Tclient = Client(ACCOUNT_SID, AUTH_TOKEN)

    verify_check = Tclient.verify.services('VAc59c05709ed6664de8094e279a53fb1f').verification_checks.create(to=mobile_no, code=received)

    if verify_check.status == 'pending':
        return render_template('otp_error.html')
    else:
        return render_template('doc.html')


@app.route('/token')
def generate_token(): 
    TWILIO_ACCOUNT_SID = 'AC291104b9da0c838324afb38b6271fb9b'
    TWILIO_SYNC_SERVICE_SID = 'IS2936995dabef3bac2fd1e20a5894d953'
    TWILIO_API_KEY = 'SKbed290f2a04b5c1bcb46d9b860338844'
    TWILIO_API_SECRET = 'TutyS6xw8QjiFfKKRyqQfC5hg6XmHlqZ'

    username = request.args.get('username', fake.user_name())
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

if __name__ == '__main__':
    app.run(debug=True)