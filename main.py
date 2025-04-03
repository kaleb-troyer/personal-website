
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, request
from model import PageVisit, Visitors, logUser
from flask_sqlalchemy import SQLAlchemy

import getinfo
import os

# instantiating database
db = SQLAlchemy()

# instantiating the webapp
app = Flask(__name__)

# webapp configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(__file__), 'database.db')}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)

db.init_app(app)
with app.app_context():
    db.create_all()

# website page routines
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home(page=None):

    user = logUser(db, "home")
    if not user:
        return render_template("404.html"), 404

    skills = getinfo.getSkills()
    software = getinfo.getSoftware()
    education = getinfo.getEducation()
    experience = getinfo.getExperience()
    introduction = getinfo.getAbout()["home page"]

    return render_template(
        "home.html",
        introduction=introduction,
        skills=skills,
        software=software,
        education=education,
        work_history=experience,
        subpage=page, 
    )

@app.route("/home/<page>")
def home_subpages(page):

    if page not in ["impact", "skills", "experience"]:
        return "Page not found", 404

    skills = getinfo.getSkills()
    software = getinfo.getSoftware()
    education = getinfo.getEducation()
    experience = getinfo.getExperience()
    introduction = getinfo.getAbout()["home page"]

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(
            f"_{page}.html", 
            introduction=introduction,
            skills=skills,
            software=software,
            education=education,
            work_history=experience,
            subpage=page, 
        )

    return home(page=page)

@app.route('/design', methods=['GET'])
def design(): 

    user = logUser(db, 'design')
    if not user: 
        return render_template('404.html'), 404

    portfolio = getinfo.getPortfolio()

    return render_template(
        'portfolio.html', 
        portfolioItems=portfolio
    )

@app.route('/about', methods=['GET'])
def about(): 

    user = logUser(db, 'about')
    if not user: 
        return render_template('404.html'), 404

    about = getinfo.getAbout()
    ethos = about['ethos']
    intro = about['intro']
    interests = about['interests']

    return render_template(
        'about.html', 
        interests=interests, 
        ethos=ethos, 
        intro=intro
    )

@app.route('/analytics', methods=['GET'])
def analytics(): 

    user = logUser(db, 'analytics')
    if not user: 
        return render_template('404.html'), 404

    totalvisits   = db.session.query(PageVisit.id).count()
    totalvisitors = db.session.query(Visitors.id).count()
    lastXVisits   = db.session.query(PageVisit).order_by(PageVisit.id.desc()).limit(25).all()
    lastXVisitors = db.session.query(Visitors).order_by(Visitors.id.desc()).limit(25).all()

    analysis = {
        'Total Clicks': totalvisits,
        'Total Visitors': totalvisitors,
        'Current Visitor': str(logUser(db, 'analytics'))
    }

    return render_template(
        'analytics.html', 
        analysis=analysis, 
        lastXVisits=lastXVisits, 
        lastXVisitors=lastXVisitors
    )


if __name__=='__main__': 
    app.run(host="0.0.0.0", debug=True)

