from flask import render_template, request, Blueprint, url_for, redirect
from yogapose import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy')

@main.route("/terms_of_service")
def terms_of_service():
    return render_template('terms_of_service.html', title='Terms of Service')

@main.route("/impressum")
def impressum():
    return render_template('impressum.html', title='Contact and Legal Notice')