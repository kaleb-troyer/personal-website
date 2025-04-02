
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request

import urllib.request
import json
import pytz
import re

db = SQLAlchemy()

class PageVisit(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    page_id = db.Column(db.String(40), index = True, unique = False, nullable = False)
    datetime = db.Column(db.DateTime, index = True, unique = False, nullable = True)

    def __repr__(self):
        return f"#{self.id} | visitor {self.visitor_id} @ {str(self.datetime)[:-7]} | {self.page_id} page"

class Visitors(db.Model):

    id = db.Column(db.Integer, primary_key = True, index = True, autoincrement = True)
    totalvisits = db.Column(db.Integer, index = True, unique = False, nullable = False)
    ip_address = db.Column(db.String(20), index = False, unique = True, nullable = False)
    location = db.Column(db.String(120), index = True, unique = False, nullable = True)
    lasttime = db.Column(db.DateTime, index = True, unique = False, nullable = True)  
    pagevisits = db.relationship('PageVisit', backref = 'visitors', lazy = True)

    def __repr__(self):
        return f"visitor {self.id} | {self.lasttime} | {self.location}"

def _validate_ip(ip): 
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    # Check if the input matches the IP address pattern
    if re.match(pattern, ip):
        parts = ip.split('.')
        if all(0 <= int(part) <= 255 for part in parts):
            return True

    return False

def logUser(db, page):
    '''
    Records a user visit at the given page. The record is 
    saved to an SQL database. If the user has visited before, 
    their number of visits is incremented by one. 

    If the ip is not of the valid format or originates from
    a country on the blacklist, the function returns false. 
    '''

    current_utc_time = datetime.now(pytz.utc)
    cst_time_zone = pytz.timezone('America/Chicago')
    current_cst_time = current_utc_time.astimezone(cst_time_zone)
    now = current_cst_time
    page_id = str(page)

    try: # retrieving location information from the visitor ip address
        
        # getting the visitor ip address
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip_address = request.environ['REMOTE_ADDR'].split(',')[0]
        else:
            ip_address = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
        if _validate_ip(ip_address): 
            pass
        else: return False

        # location information as json from ipinfo.io
        url = f'http://ipinfo.io/{ip_address}/json'
        with urllib.request.urlopen(url) as response:
            location_json = json.load(response)
        city = location_json.get('city', '')
        state = location_json.get('region', '')
        country = location_json.get('country', '')
        location = f'{city}, {state}, {country}'

        # blacklisting by region
        ban_list = ['CN', 'RU', 'IR', 'UA', 'HK']
        if country in ban_list: 
            return False

    except Exception:
        ip_address = "ip not acquired"
        location = "location not acquired"
        print(Exception())

    # retrieving the visitor from the database if they exist
    visitor = db.session.query(Visitors).filter(Visitors.ip_address == ip_address).first()
    
    # if the visitor exists, record the visit
    if visitor:
        visitor.lasttime = now
        visitor.totalvisits += 1

    # else, create a new visitor
    else:
        visitor = Visitors(
            totalvisits = 1,
            ip_address = ip_address,
            location = location,
            lasttime = now
        )

        db.session.add(visitor)
        try: db.session.commit()
        except Exception:
            db.session.rollback()
            print(Exception())

    # recording the page visit
    visit = PageVisit(
        visitor_id = visitor.id,
        page_id = page_id,
        datetime = now
    )

    # save the page visit to the database
    db.session.add(visit)
    try: db.session.commit()
    except Exception:
        db.session.rollback()
        print(Exception())

    return visitor



