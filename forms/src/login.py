from flask import Blueprint, redirect

login_blueprint = Blueprint('login', __name__)

base_url = app.config.get('API_DOMAIN')

@login_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template(
            "register.html"
        )
    elif request.method == 'POST':
        # get user form data
        email = request.form.get('email')
        password = request.form.get('password')

        # send post request to the server
        url = f'{base_url}/auth/register'
        response = requests.post(url,
            json={
                'email': email,
                'password': password
            }
        )

        if response.status_code == 201:
            auth_token = response.json().get('auth_token')
            app.config['AUTH_TOKEN'] = auth_token
            return redirect(url_for('index'), code=303)

        # display an error message
        print(response.json().get('message'))
        return redirect(url_for('login.register'), code=303)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    pass

@login_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
