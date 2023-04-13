# Add Google Login to your Flask app
A flask app to simplify adding **Google** Login using [oauthlib](https://github.com/oauthlib/oauthlib) module.
<br>
The steps in the Flask app are structured based on what I think will help any one implemeting Google login with oauthlib with `CLIENT_ID`, `CLIENT_SECRET` & `redirect_uri` generated from the **Google** developer console.

## How to setup:
- Create a Python virtual environment

```
python3 -m venv ~/add_google_login
```

- Activate the virtual environment

```
source ~/add_google_login/bin/activate
```

- Install the packages from the `requirements.txt` file

```
python -m pip install -r requirements.txt
```

- Run the Flask app

```
python sso_google_oauth.py
```

