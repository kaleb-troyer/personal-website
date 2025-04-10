
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, request
from model import PageVisit, Visitors, logUser
from flask_sqlalchemy import SQLAlchemy
from markdown import markdown as md

import getinfo
import dotenv
import os

# loading environment variables
dotenv.load_dotenv()

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

    impact = getinfo.getImpact()
    skills = getinfo.getSkills()
    software = getinfo.getSoftware()
    languages = getinfo.getLanguages()
    education = getinfo.getEducation()
    experience = getinfo.getExperience()
    introduction = getinfo.getAbout()["home page"]

    return render_template(
        "home.html",
        introduction=introduction,
        impact=impact, 
        skills=skills,
        software=software,
        languages=languages, 
        education=education,
        experience=experience,
        subpage=page, 
    )

@app.route('/design', methods=['GET'])
def design(): 

    user = logUser(db, 'design')
    if not user: 
        return render_template('404.html'), 404

    portfolio = getinfo.getPortfolio()
    introduction = getinfo.getAbout()["design note"]

    return render_template(
        'portfolio.html', 
        introduction=introduction, 
        portfolioItems=portfolio
    )

@app.route('/about', methods=['GET'])
def about(page=None): 

    user = logUser(db, 'about')
    if not user: 
        return render_template('404.html'), 404

    aboutme = getinfo.getAbout()
    ethos = aboutme['ethos']
    intro = aboutme['intro']
    interests = aboutme['interests']
    likes = getinfo.getLikes()
    uses = getinfo.getUses()

    return render_template(
        'about.html', 
        interests=interests, 
        ethos=ethos, 
        intro=intro, 
        likes=likes, 
        uses=uses, 
        subpage=page
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

@app.route("/home/<page>")
def subpages_home(page):

    if page not in ["impact", "skills", "experience", "education"]:
        return "Page not found", 404

    impact = getinfo.getImpact()
    skills = getinfo.getSkills()
    software = getinfo.getSoftware()
    languages = getinfo.getLanguages()
    education = getinfo.getEducation()
    experience = getinfo.getExperience()
    introduction = getinfo.getAbout()["home page"]

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        
        user = logUser(db, f'home/{page}')
        if not user: 
            return render_template('404.html'), 404

        return render_template(
            f"subpages/_{page}.html", 
            introduction=introduction,
            impact=impact, 
            skills=skills,
            software=software,
            languages=languages, 
            education=education,
            experience=experience,
            subpage=page, 
        )

    return home(page=page)

@app.route("/about/<page>")
def subpages_about(page):

    if page not in ["interests", "likes", "uses"]:
        return "Page not found", 404

    aboutme = getinfo.getAbout()
    ethos = aboutme['ethos']
    intro = aboutme['intro']
    interests = aboutme['interests']
    likes = getinfo.getLikes()
    uses = getinfo.getUses()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        
        user = logUser(db, f'about/{page}')
        if not user: 
            return render_template('404.html'), 404
        
        return render_template(
            f"subpages/_{page}.html", 
            interests=interests, 
            ethos=ethos, 
            intro=intro,
            likes=likes, 
            uses=uses, 
            subpage=page
        )

    return about(page=page)


if __name__=='__main__': 
    app.run(host="0.0.0.0", debug=False)
