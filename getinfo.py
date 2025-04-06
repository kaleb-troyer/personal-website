
import json
import os

def _ed_bar(value, max): 
    return 100 * (value / max)

def _xp_bar(value, max): 
    return 100 * (value / max)


def _getter(name, folder='profile'):

    path = os.path.join(os.getcwd(), folder)
    file = f'{name}.json'
    with open(os.path.join(path, file), 'r', encoding='utf-8') as file: 
        data = json.load(file)

    return data

def getSkills(): 
    
    skills = _getter('skills')
    software = _getter('software')
    languages = _getter('languages')

    categories = [skills, software, languages]
    maxed = max(entry['education'] for field in categories for entry in field)
    maxxp = max(entry['hours'] for field in categories for entry in field)
    for entry in skills: 
        entry['education'] = _ed_bar(entry['education'], maxed)
        entry['experience'] = _xp_bar(entry['hours'], maxxp)

    return skills

def getSoftware(): 

    skills = _getter('skills')
    software = _getter('software')
    languages = _getter('languages')

    categories = [skills, software, languages]
    maxed = max(entry['education'] for field in categories for entry in field)
    maxxp = max(entry['hours'] for field in categories for entry in field)
    for entry in software: 
        entry['education'] = _ed_bar(entry['education'], maxed)
        entry['experience'] = _xp_bar(entry['hours'], maxxp)

    return software

def getLanguages(): 

    skills = _getter('skills')
    software = _getter('software')
    languages = _getter('languages')

    categories = [skills, software, languages]
    maxed = max(entry['education'] for field in categories for entry in field)
    maxxp = max(entry['hours'] for field in categories for entry in field)
    for entry in languages: 
        entry['education'] = _ed_bar(entry['education'], maxed)
        entry['experience'] = _xp_bar(entry['hours'], maxxp)

    return languages

def getEducation(): 
    return _getter('education')

def getExperience(): 
    return _getter('experience')

def getPortfolio(): 
    return _getter('portfolio')

def getAbout(): 
    return _getter('about')

if __name__=='__main__': 

    loaded_json = getAbout()['introduction']
    print(loaded_json)
