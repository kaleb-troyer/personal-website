
import json
import os

# def _ed_bar(value, max, length=10): 
#     strbar = round(length * value / max)
#     return "▰" * int(strbar)

# def _xp_bar(value, max, length=24): 
#     strbar = round(length * value / max)
#     return f"{value:0>{len(str(max))}}\t{"▰" * (int(strbar))}"

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

    maxed = max([entry['education'] for entry in skills] + [entry['education'] for entry in software])
    maxxp = max([entry['hours'] for entry in skills] + [entry['hours'] for entry in software])
    for entry in skills: 
        entry['education'] = _ed_bar(entry['education'], maxed)
        entry['experience'] = _xp_bar(entry['hours'], maxxp)

    return skills

def getSoftware(): 

    skills = _getter('skills')
    software = _getter('software')

    maxed = max([entry['education'] for entry in skills] + [entry['education'] for entry in software])
    maxxp = max([entry['hours'] for entry in skills] + [entry['hours'] for entry in software])
    for entry in software: 
        entry['education'] = _ed_bar(entry['education'], maxed)
        entry['experience'] = _xp_bar(entry['hours'], maxxp)

    return software

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
