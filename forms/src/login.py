from flask import Blueprint

login_blueprint = Blueprint('login', __name__)

api_domain = app.config.get('API_DOMAIN')

@login_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template(
            "register.html"
        )
    elif request.method == 'POST':
        response = requests.get()

        # get user form data
        email = request.form.get('email')
        password = request.form.get('password')



        # validate the email and password
        try:
            User.validate_email(email)
        except AssertionError:
            # display a message on the page
            print("Invalid email format.")
            redirect(url_for('forms.register_form'))# status code for redirect with error?
        # check that the email is not already in use
        if User.query.filter_by(email=email).first():
            print("That email is already taken. Please try again.")
            redirect(url_for('forms.register_form'))# status code for redirect with error?

        # if unsuccessful, display an error message and redirect to register page

        # if successful, log them in and redirect to the home page
        new_user = User(email=email, password=password)
        # TODO: determine if an auth_token is necessary for the forms views
        auth_token = user.encode_auth_token(
            expiration_seconds=int(current_app.config.get('TOKEN_EXPIRATION', 10)))
        db.session.add(new_user)
        db.session.commit()
        # add auth token to response?
        return redirect(url_for('forms.forms_index'), code=303)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # get auth token from headers
        auth_token = request.headers.get('Authorization').split(' ')[-1]
        user = User.query.filter_by(email=email).first()
        if not user:
            print("Email not found. Please try again.")
            redirect(url_for('forms.login_form'))
        try:
            user.validate_password()
        except AssertionError:
            print("Invalid password. Please try again.")
            redirect(url_for('forms.login_form'))
        auth_token = user.encode_auth_token(
            expiration_seconds=int(current_app.config.get('TOKEN_EXPIRATION', 10))
        )

@login_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
