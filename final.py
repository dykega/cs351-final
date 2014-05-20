from flask import Flask, render_template, request, session, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import *
from flask_bootstrap import Bootstrap
import os
import urllib
import datetime

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

SkillProject = db.Table('skillprojects',
    db.Column('skillName', db.Text, db.ForeignKey('skill.skillName')),
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
    projects = db.relationship('Project', secondary= UserProject)

class Skill(db.Model):
    __tablename__ = 'skill'
    skillName = db.Column(db.Text, primary_key=True)
    users = db.relationship('User', secondary = UserSkill)
    projects = db.relationship('Project', secondary=SkillProject)

class Project(db.Model):
    __tablename__ = 'project'
    projectId = db.Column(db.Text, primary_key=True)
    projectName = db.Column(db.Text)
    projectDesc = db.Column(db.Text)
    projectDue = db.Column(db.Text)
    projectStart = db.Column(db.Date)
    projectEnd = db.Column(db.Date)
    contributers = db.relationship('User', secondary = UserProject)
    skills = db.relationship('Skill', secondary= SkillProject)

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
s10 = Skill(skillName='marketing',users=[u2,u3,u5])
s11 = Skill(skillName='pricing')

db.session.add_all([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11])

p1 = Project(projectId="IntProgFinal-01", projectName="Internet Programming Final", projectDesc="A final project for Internet Programming class for spring semester 2014",projectDue="5-21-2014",projectStart=datetime.date(2014,5,1),projectEnd=datetime.date(2014,5,20),contributers=[u1,u2,u3],skills=[s1,s2,s6,s7])
p2 = Project(projectId="IntProg-01", projectName="Internet Programming Class", projectDesc="Attend Internet Programming Class",projectDue="5-18-2014",projectStart = datetime.date(2014,2,5),projectEnd=datetime.date(2014,5,22),contributers=[u1,u2,u3,u5],skills=[s1,s2,s6,s7,s9])
p3 = Project(projectId="Startup-01", projectName="New Startup", projectDesc="Create a new startup company to work for after graduation",projectDue="5-30-2015",projectStart = datetime.date(2014,5,15), projectEnd=datetime.date(2014,6,10),contributers=[u4,u5],skills=[s8,s10,s11])

db.session.add_all([p1,p2,p3])
db.session.commit()

class SkillForm(Form):
    skill = TextField('Skill')

class UserForm(Form):
    name = TextField('Name of User')

class addUserForm(Form):
    firstname = TextField("First Name")
    lastname = TextField("First Name")
    nickname = TextField("First Name")
    email = TextField("First Name")
    address = TextField("First Name")
    phoneNum = TextField("Phone Number")
    skills = TextField("First Name")


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
            projList = useList.projects
            useList = useList.users
        else:
            projList = []
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

        projResults = []
        if len(projList) > 8: # limit results to 8 entries
            projList = projList[0:8]
        for resProj in projList:
            x = []
            x.append(resProj.projectId)
            x.append(resProj.projectName.title())
            x.append(resProj.projectDesc)
            sks = []
            for i in range(2):
                sks.append(resProj.skills[i].skillName.title())
            x.append(sks)
            projResults.append(x)

        return render_template('skill.html', results = results, form = form, qr = qr, projResults=projResults)
    else:
        qr = False
        return render_template('skill.html', form = form,qr=qr)

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
        user.append(usInfo.userId)
        if usInfo.firstName != None:
            user.append(usInfo.firstName.title())
        else:
            user.append("")
        if usInfo.lastName != None:
            user.append(usInfo.lastName.title())
        else:
            user.append("")
        if usInfo.nickname != None:
            user.append(usInfo.nickname.title())
        else:
            user.append("")
        user.append(usInfo.email)
        user.append(usInfo.address)
        user.append(usInfo.phoneNum)
        skills = usInfo.skills
        sks = []
        for s in skills:
            sks.append(s.skillName.title())
        user.append(sks)
        projects = usInfo.projects
        pjs = []
        for p in projects:
            pInfo = []
            pInfo.append(p.projectId)
            pInfo.append(p.projectName.title())
            pjs.append(pInfo)
        user.append(pjs)
        print user
        #user list: 0-userid, 1-firstname, 2-lastname, 3-nickname, 4-email, 5-address, 6-phoneNum, 7-skills, 8-projects
        #skill list: 0-skillName
        #project list: 0-projectId, 1-project name
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
        cps.append(c.email)
        contr.append(cps)
    project.append(contr)
    sklRaw = projRaw.skills
    sklls = []
    for s in sklRaw:
        sklls.append(s.skillName)
    project.append(sklls)
    complete = int(100*(((datetime.date.today() - projRaw.projectStart).days * 1.0) / (projRaw.projectEnd - projRaw.projectStart).days))
    return render_template('projProfile.html',project=project,complete=complete)

@app.route('/api')
def api():
    if request.args.get("user") != None:
        if request.args.get("type") != None:
            if request.args.get("type").lower() == "first":
                inName = request.args.get('user').lower()
                usRaw = User.query.filter_by(firstName=inName).all()
                res = []
                for us in usRaw:
                    u = []
                    u.append(us.firstName)
                    u.append(us.lastName)
                    u.append(us.nickname)
                    sksRaw = us.skills
                    sks = []
                    for s in sksRaw:
                        sks.append(s.skillName)
                    u.append(sks)
                    res.append(u)
                return jsonify(results=res)

            elif request.args.get("type").lower() == "last":
                inName = request.args.get('user').lower()
                usRaw = User.query.filter_by(lastName=inName).all()
                res = []
                for us in usRaw:
                    u = []
                    u.append(us.firstName)
                    u.append(us.lastName)
                    u.append(us.nickname)
                    sksRaw = us.skills
                    sks = []
                    for s in sksRaw:
                        sks.append(s.skillName)
                    u.append(sks)
                    res.append(u)
                return jsonify(results=res)

            elif request.args.get("type").lower() == "nickname":
                inName = request.args.get('user').lower()
                usRaw = User.query.filter_by(nickname=inName).all()
                res = []
                for us in usRaw:
                    u = []
                    u.append(us.firstName)
                    u.append(us.lastName)
                    u.append(us.nickname)
                    sksRaw = us.skills
                    sks = []
                    for s in sksRaw:
                        sks.append(s.skillName)
                    u.append(sks)
                    res.append(u)
                return jsonify(results=res)

            else: 
                return jsonify(results="ERROR:Incorrect Type specified")
        else:
            inName = request.args.get('user').lower()
            usRaw1 = User.query.filter_by(firstName=inName).all()
            usRaw2 = User.query.filter_by(lastName=inName).all()
            usRaw3 = User.query.filter_by(nickname=inName).all()
            usRaw = usRaw1 + usRaw2 + usRaw3
            res = []
            for us in usRaw:
                u = []
                u.append(us.firstName)
                u.append(us.lastName)
                u.append(us.nickname)
                sksRaw = us.skills
                sks = []
                for s in sksRaw:
                    sks.append(s.skillName)
                u.append(sks)
                res.append(u)
            return jsonify(results=res)
    else:
        return jsonify(results="ERROR: Specify User")   

@app.route('/useradd')
def add():
