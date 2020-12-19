# yogapose
Yoga pose web app with user accounts

- requirements.txt: This has been generated by _pip freeze > requirements.txt_. mod_wsgi needs to be installed additionally with _pip install mod_wsgi_ (doesn't get included/installedautomatically for some reason)

- robots.txt: Standard robots.txt file for Google's bots

- run.py: This create's the flask app

- yogapose/: This folder contains the source code for the flask app

- yogapose.wsgi: This is the wsgi script needed for the apache webserver's configuration file. Before going live, the flask app can be tested by running this script file with _mod_wsgi-express start-server yogapose.wsgi_

- inference.py: Needed for fastai's load_learner to work properly (user-defined functions like _get_x_ and _get_y_ will be imported from here)

Package structure:
-----------------
```
YogaPose
├── README.md
├── inference.py
├── requirements.txt
├── robots.txt
├── run.py
├── tree.txt
├── yogapose
│   ├── __init__.py
│   ├── config.py
│   ├── errors
│   │   ├── __init__.py
│   │   └── handlers.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models.py
│   ├── pkls
│   │   └── y82-resnet18-multi.pkl
│   ├── posts
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── site.db
│   ├── static
│   │   ├── main.css
│   │   └── posted_pics
│   ├── templates
│   │   ├── about.html
│   │   ├── account.html
│   │   ├── errors
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   ├── 413.html
│   │   │   └── 500.html
│   │   ├── home.html
│   │   ├── impressum.html
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── post.html
│   │   ├── privacy_policy.html
│   │   ├── register.html
│   │   ├── reset_request.html
│   │   ├── reset_token.html
│   │   ├── terms_of_service.html
│   │   ├── update_post.html
│   │   └── user_posts.html
│   └── users
│       ├── __init__.py
│       ├── forms.py
│       ├── routes.py
│       └── utils.py
└── yogapose.wsgi
```
