from flask import Flask, render_template, request, session
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import *
from flask_bootstrap import Bootstrap
import os
import urllib

app = Flask(__name__)
app.debug = True   # need this for autoreload as well as stack trace
app.secret_key = 'chelseafc'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

Bootstrap(app)

db = SQLAlchemy(app)

UserSkill = db.Table('userskills',
    db.Column('user_Id', db.Text, db.ForeignKey('user.userId')),
    db.Column('skill_Name', db.Text, db.ForeignKey('skill.skillName'))
)

UserProject = db.Table('userprojects',
    db.Column('user_Id', db.Text, db.ForeignKey('user.userId')),
    db.Column('project_Id', db.Text, db.ForeignKey('project.projectId'))
)

class User(db.Model):
    __tablename__='user'
    userId = db.Column(db.Text, primary_key=True)
    firstName = db.Column(db.Text)
    lastName = db.Column(db.Text)
    nickname = db.Column(db.Text)
    email = db.Column(db.Text)
    address = db.Column(db.Text)
    phoneNum = db.Column(db.Text)
    skills = db.relationship('Skill', secondary = UserSkill)

class Skill(db.Model):
    __tablename__ = 'skill'
    skillName = db.Column(db.Text, primary_key=True)
    users = db.relationship('User', secondary = UserSkill)

class Project(db.Model):
    __tablename__ = 'project'
    projectId = db.Column(db.Text, primary_key=True)
    projectName = db.Column(db.Text)
    projectDesc = db.Column(db.Text)
    projectDue = db.Column(db.Text)
    contributers = db.relationship('User', secondary = UserProject)

db.drop_all()
db.create_all()

u1 = User(userId='krogis01',firstName='isabelle',lastName='krogh',nickname = "elle", email='krogis01@luther.edu',address='Farwell 237',phoneNum='515-401-7985')
u2 = User(userId='junghe02',firstName='henry',lastName='jungbauer',nickname = "hank",email='junghe02@luther.edu',address='Dieseth 523',phoneNum='651-925-7403')
u3 = User(userId='dykega01',firstName='gage',lastName='dykema',nickname = "gagey",email='dykega01@luther.edu',address='Larsen APT',phoneNum='651-249-7599')
u4 = User(userId='gagehe01',firstName='henry',lastName='gage',email='gagehe01@luther.edu',address='Miller 218',phoneNum='651-249-7599')
u5 = User(userId='bmiller', firstName='brad',lastName='miller',email='bmiller@luther.edu',address='Olin 321',phoneNum='563-387-1137')
u6 = User(userId='bottth01',firstName='thomas',lastName='bottem',nickname = "tom",email='bottth01@luther.edu',address='Larsen APT',phoneNum='555-679-7891')

db.session.add_all([u1,u2,u3,u4,u5,u6])

s1 = Skill(skillName='html',users=[u1,u2,u3,u4,u5,u6])
s2 = Skill(skillName='python',users=[u1,u2,u3,u5])
s3 = Skill(skillName='german',users=[u2,u4])
s4 = Skill(skillName='swedish',users=[u3,u6])
s5 = Skill(skillName='chinese',users=[u1,u4])
s6 = Skill(skillName='css',users=[u3,u5])
s7 = Skill(skillName='internet programming',users=[u2,u3,u5])
s8 = Skill(skillName='business',users=[u6])
s9 = Skill(skillName='teaching',users=[u6,u5])

db.session.add_all([s1,s2,s3,s4,s5,s6,s7,s8,s9])

p1 = Project(projectId="IntProgFinal-01", projectName="Internet Programming Final", projectDesc="A final project for Internet Programming class for spring semester 2014",projectDue="5-21-2014",contributers=[u1,u2,u3])
p2 = Project(projectId="IntProg-01", projectName="Internet Programming Class", projectDesc="Attend Internet Programming Class",projectDue="5-18-2014",contributers=[u1,u2,u3,u5])
p3 = Project(projectId="Startup-01", projectName="New Startup", projectDesc="Create a new startup company to work for after graduation",projectDue="5-30-2015",contributers=[u4,u5])

db.session.add_all([p1,p2,p3])
db.session.commit()

class SkillForm(Form):
    skill = TextField('Skill')

class UserForm(Form):
    name = TextField('Name of User')
    

@app.route('/') 
def home():
    return render_template('main.html')

@app.route('/skills')
def skillsearch():
    form = SkillForm()
    if request.args.get("skill") != None:
        qr = True
        results = []
        inskill = request.args.get('skill').lower()
        useList = Skill.query.filter_by(skillName = inskill).first()
        if useList != None:
            useList = useList.users
        else:
            useList = []
        if len(useList) > 8: # limit results to 8 entries
            useList = useList[0:8]
        for resUser in useList: #convert querry to list
            x = []
            x.append(resUser.userId)
            if resUser.firstName != None:
                x.append(resUser.firstName.title())
            else:
                x.append("")
            if resUser.lastName != None:
                x.append(resUser.lastName.title())
            else:
                x.append("")            
            if resUser.nickname != None:
                x.append(resUser.nickname.title())
            else:
                x.append("")
            x.append(resUser.email)
            x.append(resUser.address)
            x.append(resUser.phoneNum)
            sks = []
            urlSks =  []
            for i in range (4):
                try:
                    s = resUser.skills[i].skillName.title()
                except:
                    s = ""
                try:
                    urlS = urllib.quote_plus(resUser.skills[i].skillName)
                except:
                    urlS = s.lower()
                sks.append(s)
                urlSks.append(urlS)
            x.append(sks)
            x.append(urlSks)
            results.append(x)
        return render_template('skill.html', results = results, form = form, qr = qr)
    else:
        return render_template('skill.html', form = form)

@app.route('/users')
def usersearch():
    form = UserForm()
    if request.args.get("name") != None:
        qr = True
        results = []
        namesStr = request.args.get('name').lower()
        names = namesStr.split()
        resList = []
        useList = []
        for inname in names:
            resList1 = User.query.filter_by(firstName = inname).all()
            resList2 = User.query.filter_by(lastName = inname).all()
            resList3 = User.query.filter_by(nickname = inname).all()
            resList = resList + resList1 + resList2 + resList3
        unique = set()
        for x in resList:
            if x not in unique:
                unique.add(x)
                useList.append(x)
        if len(useList) > 8: # limit results to 8 entries
            useList = useList[0:8]
        for resUser in useList: #convert querry to list
            x = []
            x.append(resUser.userId)
            if resUser.firstName != None:
                x.append(resUser.firstName.title())
            else:
                x.append("")                
            if resUser.lastName != None:
                x.append(resUser.lastName.title())
            else:
                x.append("")
            if resUser.nickname != None:
                x.append(resUser.nickname.title())
            else:
                x.append("")
            x.append(resUser.email)
            x.append(resUser.address)
            x.append(resUser.phoneNum)
            results.append(x)
        return render_template('users.html', results = results, form = form, qr = qr)
    else:
        return render_template('users.html', form = form)

@app.route('/users/<userid>')
def userprofile(userid):
    user = []
    usInfo = User.query.filter_by(userId = userid).first()
    if usInfo != None:
        if user.append(usInfo.firstName) != None:
            user.append(usInfo.firstName).title()
        else:
            user.append("")
        if user.append(usInfo.lastName) != None:
            user.append(usInfo.lastName).title()
        else:
            user.append("")
        if user.append(usInfo.nickname) != None:
            user.append(usInfo.nickname).title()
        else:
            user.append("")
        user.append(usInfo.email)
        user.append(usInfo.address)
        user.append(usInfo.phoneNum)
        skills = usInfo.skills
        sks = []
        for s in skills:
            sks.append(s.skillName)
        user.append(sks)
    else:
        user = []
    return render_template('profile.html', user=user)

@app.route('/projects')
def projects():
    projs = Project.query.limit(5)
    projects = []
    for p in projs:
        ip = []
        ip.append(p.projectId)
        ip.append(p.projectName)
        ip.append(p.projectDesc)
        ip.append(p.projectDue)
        contrRaw = p.contributers
        contr = []
        for c in contrRaw:
            cps = []
            cps.append(c.userId)
            cps.append(c.firstName)
            cps.append(c.lastName)
            contr.append(cps)
        ip.append(contr)
        projects.append(ip)
    return render_template('project.html',projects=projects)

@app.route('/projects/<projectid>')
def projectProfile(projectid):
    projRaw = Project.query.filter_by(projectId=projectid).first()
    project = []
    print projRaw
    project.append(projRaw.projectId)
    project.append(projRaw.projectName)
    project.append(projRaw.projectDesc)
    project.append(projRaw.projectDue)
    contrRaw = projRaw.contributers
    contr = []
    for c in contrRaw:
        cps = []
        cps.append(c.userId)
        cps.append(c.firstName)
        cps.append(c.lastName)
        contr.append(cps)
    project.append(contr)
    return render_template('projProfile.html',project=project)

