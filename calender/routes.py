import calendar
import datetime
import time
import re

from flask import render_template, flash, redirect, url_for, session, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from calender import app, db
from calender.forms import LoginForm, SignupForm, AddeventsForm
from calender.models import User, Event


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash("User is not found: {}".format(form.username.data))
            return redirect(url_for('login'))
        if check_password_hash(user_in_db.password_hash, form.password.data):
            session["USERNAME"] = user_in_db.username
            session["DATENOW"] = time.strftime("%Y-%m-%d", time.localtime())
            now = datetime.datetime.now()
            weeknum = now.isoweekday()
            startweek = now + datetime.timedelta(days=-weeknum + 1)
            session["STARTWEEK"] = startweek.strftime("%Y-%m-%d")
            monthtest = startweek.month
            yeartest = startweek.year
            session["STARTMONTH"] = monthtest
            session["STARTYEAR"] = yeartest
            session["DAYVIEW"] = "DAILY"
            session["TYPE"] = "ALL"
            return render_template('home.html', user=user_in_db)
        flash('Incorrect Password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Log In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash("Please enter matched passwords !!!")
            return redirect(url_for('signup'))
        pass_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=pass_hash)
        db.session.add(user)
        db.session.commit()
        session["USERNAME"] = user.username
        return render_template('index.html', user=user)
    return render_template('signup.html', title='New Register', form=form)


@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    form = AddeventsForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            datenow = form.date.data
            dateTime = form.time.data
            category = form.category.data
            event = form.event.data
            user = User.query.filter(User.username == session.get("USERNAME")).first()
            newevent = Event(date=datenow, time=dateTime, category=category, event=event, author=user)
            db.session.add(newevent)
            db.session.commit()
            return render_template("home.html", user=user)
        else:
            return render_template('addcalender.html', title='Add new', form=form)
    else:
        flash("You need to either login or signup first")
        return redirect(url_for('addnew'))


@app.route('/back')
def back():
    user = User.query.filter(User.username == session.get("USERNAME")).first()
    return render_template('home.html', user=user)


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('index'))


@app.route('/listall')
def listall():
    user = User.query.filter(User.username == session.get("USERNAME")).first()
    events = Event.query.filter(Event.user_id == user.id).order_by(Event.date).all()
    session["TYPE"] = "ALL"
    dayview = session.get("DAYVIEW")
    if dayview == "DAILY":
        return redirect(url_for("daily"))
    elif dayview == "WEEKLY":
        return redirect(url_for("weekly"))
    elif dayview == "MONTHLY":
        return redirect(url_for("monthly"))
    else:
        return render_template('eventslist.html', title='List All', events=events)


@app.route('/listevents')
def listevents():
    user = User.query.filter(User.username == session.get("USERNAME")).first()
    events = Event.query.filter(Event.user_id == user.id, Event.category == '0').order_by(Event.date).all()
    session["TYPE"] = "EVENTS"
    dayview = session.get("DAYVIEW")
    if dayview == "DAILY":
        return redirect(url_for("daily"))
    elif dayview == "WEEKLY":
        return redirect(url_for("weekly"))
    elif dayview == "MONTHLY":
        return redirect(url_for("monthly"))
    else:
        return render_template('eventslist.html', title='Events', events=events)


@app.route('/listdeadlines')
def listdeadlines():
    user = User.query.filter(User.username == session.get("USERNAME")).first()
    events = Event.query.filter(Event.user_id == user.id, Event.category == '1').order_by(Event.date).all()
    session["TYPE"] = "DEADLINE"
    dayview = session.get("DAYVIEW")
    if dayview == "DAILY":
        return redirect(url_for("daily"))
    elif dayview == "WEEKLY":
        return redirect(url_for("weekly"))
    elif dayview == "MONTHLY":
        return redirect(url_for("monthly"))
    else:
        return render_template('eventslist.html', title='DeadLine', events=events)


@app.route('/daily')
def daily():
    user = User.query.filter(User.username == session.get("USERNAME")).first()
    session["DAYVIEW"] = "DAILY"
    if not session.get("TYPE") is None:
        if not session.get("DATENOW") is None:
            date = session.get("DATENOW")
            type = session.get("TYPE")
            if type == "ALL":
                events = Event.query.filter(Event.user_id == user.id, Event.date == date).order_by(Event.time).all()
                return render_template('daily.html', title="List All at " + date, events=events, localdate=date)
            elif type == "EVENTS":
                events = Event.query.filter(Event.user_id == user.id, Event.date == date,
                                            Event.category == '0').order_by(Event.time).all()
                return render_template('daily.html', title="Events at " + date, events=events, localdate=date)
            else:
                events = Event.query.filter(Event.user_id == user.id, Event.date == date,
                                            Event.category == '1').order_by(Event.time).all()
                return render_template('daily.html', title="Deadlines at " + date, events=events, localdate=date)
        else:
            date = time.strftime("%Y-%m-%d", time.localtime())
            events = Event.query.filter(Event.user_id == user.id, Event.date == date).order_by(Event.date).all()
            return render_template('daily.html', title="Date is not changed, find the reason !", events=events,
                                   localdate=date)
    else:
        events = Event.query.filter(Event.user_id == user.id).order_by(Event.date).all()
        return render_template('eventslist.html', title="List All", events=events)


@app.route('/previousday')
def previousday():
    datenow = session.get("DATENOW")
    newdate = datetime.datetime.strptime(datenow, "%Y-%m-%d") + datetime.timedelta(days=-1)
    session["DATENOW"] = newdate.strftime("%Y-%m-%d")
    return redirect(url_for('daily'))


@app.route('/nextday')
def nextday():
    datenow = session.get("DATENOW")
    newdate = datetime.datetime.strptime(datenow, "%Y-%m-%d") + datetime.timedelta(days=+1)
    session["DATENOW"] = newdate.strftime("%Y-%m-%d")
    return redirect(url_for('daily'))


@app.route('/weekly')
def weekly():
    user = User.query.filter(User.username == session.get("USERNAME")).first()
    session["DAYVIEW"] = "WEEKLY"
    if not session.get("STARTWEEK") is None:
        startweek = session.get("STARTWEEK")
        type = session.get("TYPE")
        endweek1 = datetime.datetime.strptime(startweek, "%Y-%m-%d") + datetime.timedelta(days=+6)
        endweek = endweek1.strftime("%Y-%m-%d")
        weeks = []
        for i in range(7):
            daydate = datetime.datetime.strptime(startweek, "%Y-%m-%d") + datetime.timedelta(days=+i)
            day = daydate.strftime("%Y-%m-%d")
            weeks.append(day)
        if type == "ALL":
            events = Event.query.filter(Event.user_id == user.id, Event.date >= startweek,
                                        Event.date <= endweek).order_by(Event.date, Event.time).all()
            return render_template('weekly.html', title="List All from " + startweek + " to " + endweek, events=events,
                                   weeks=weeks)
        elif type == "EVENTS":
            events = Event.query.filter(Event.user_id == user.id, Event.date >= startweek, Event.date <= endweek,
                                        Event.category == '0').order_by(Event.date, Event.time).all()
            return render_template('weekly.html', title="Events at " + startweek + " to " + endweek, events=events,
                                   weeks=weeks)
        else:
            events = Event.query.filter(Event.user_id == user.id, Event.date >= startweek, Event.date <= endweek,
                                        Event.category == '1').order_by(Event.date, Event.time).all()
            return render_template('weekly.html', title="Deadlines at " + startweek + " to " + endweek, events=events,
                                   weeks=weeks)
    else:
        flash("No start week, please check out !!!")
        return redirect(url_for('weekly'))


@app.route('/previousweek')
def previousweek():
    startweek = session.get("STARTWEEK")
    newdate = datetime.datetime.strptime(startweek, "%Y-%m-%d") + datetime.timedelta(days=-7)
    session["STARTWEEK"] = newdate.strftime("%Y-%m-%d")
    return redirect(url_for('weekly'))


@app.route('/nextweek')
def nextweek():
    startweek = session.get("STARTWEEK")
    newdate = datetime.datetime.strptime(startweek, "%Y-%m-%d") + datetime.timedelta(days=+7)
    session["STARTWEEK"] = newdate.strftime("%Y-%m-%d")
    return redirect(url_for('weekly'))


@app.route('/monthly')
def monthly():
    user = User.query.filter(User.username == session.get("USERNAME")).first()
    session["DAYVIEW"] = "MONTHLY"
    if not session.get("STARTMONTH") is None and not session.get("STARTYEAR") is None:
        type = session.get("TYPE")
        startmonth = session.get("STARTMONTH")
        startyear = session.get("STARTYEAR")
        monthcalender = calendar.monthcalendar(startyear, startmonth)
        first, monthrange = calendar.monthrange(year=startyear, month=startmonth)
        startday = datetime.date(year=startyear, month=startmonth, day=1).strftime("%Y-%m-%d")
        endday = datetime.date(year=startyear, month=startmonth, day=monthrange).strftime("%Y-%m-%d")
        if type == 'ALL':
            events = Event.query.filter(Event.user_id == user.id, Event.date >= startday,
                                        Event.date <= endday).order_by(Event.date, Event.time).all()
            days = []
            for i in events:
                im = i.date
                days.append(im.day)
            days = set(days)
            return render_template('monthly.html', title="ALL " + str(startyear) + " - " + str(startmonth),
                                   monthcalender=monthcalender, events=events,
                                   days=days, startmonth=startmonth, startyear=startyear, type=type)
        elif type == 'EVENTS':
            events = Event.query.filter(Event.user_id == user.id, Event.date >= startday,
                                        Event.date <= endday, Event.category == '0').order_by(Event.date,
                                                                                              Event.time).all()
            days = []
            for i in events:
                im = i.date
                days.append(im.day)
            days = set(days)
            return render_template('monthly.html', title="Events " + str(startyear) + " - " + str(startmonth),
                                   monthcalender=monthcalender, events=events,
                                   days=days, startmonth=startmonth, startyear=startyear, type=type)
        else:
            events = Event.query.filter(Event.user_id == user.id, Event.date >= startday,
                                        Event.date <= endday, Event.category == '1').order_by(Event.date,
                                                                                              Event.time).all()
            days = []
            for i in events:
                im = i.date
                days.append(im.day)
            days = set(days)
            return render_template('monthly.html', title="Deadlines " + str(startyear) + " - " + str(startmonth),
                                   monthcalender=monthcalender, events=events,
                                   days=days, startmonth=startmonth, startyear=startyear, type=type)
    else:
        flash("No start month, Please check out")
        return redirect(url_for('monthly'))


@app.route('/previousmonth')
def previousmonth():
    startmonth = session.get("STARTMONTH")
    startyear = session.get("STARTYEAR")
    if startmonth != 1:
        newmonth = startmonth - 1
        session["STARTMONTH"] = newmonth
        return redirect(url_for('monthly'))
    else:
        newmonth = 12
        newyear = startyear - 1
        session["STARTMONTH"] = newmonth
        session["STARTYEAR"] = newyear
        return redirect(url_for('monthly'))


@app.route('/nextmonth')
def nextmonth():
    startmonth = session.get("STARTMONTH")
    startyear = session.get("STARTYEAR")
    if startmonth != 12:
        newmonth = startmonth + 1
        session["STARTMONTH"] = newmonth
        return redirect(url_for('monthly'))
    else:
        newmonth = 1
        newyear = startyear + 1
        session["STARTMONTH"] = newmonth
        session["STARTYEAR"] = newyear
        return redirect(url_for('monthly'))

# The methods below are based on the method from teachers' lectures
# I transform some structures and variables to be suitable to my project
@app.route('/checkuser', methods=['POST'])
def check_username():
    time.sleep(1)
    chosen_name = request.form.get("username")
    user_in_db = User.query.filter(User.username == chosen_name).first()
    if not user_in_db:
        return jsonify({'text': 'Username is available',
                        'returnvalue': 0})
    else:
        return jsonify({'text': 'Sorry! Username is already existed',
                        'returnvalue': 1})


@app.route('/checkloginuser', methods=['POST'])
def check_loginusername():
    time.sleep(1)
    chosen_name = request.form.get("username")
    user_in_db = User.query.filter(User.username == chosen_name).first()
    if not user_in_db:
        return jsonify({'text': 'No username, Please register first!',
                        'code': 0})
    else:
        return jsonify({'text': 'Username is ok!',
                        'code': 1})


@app.route('/checkemail', methods=['POST'])
def check_email():
    time.sleep(1)
    chosen_email = request.form.get("email")
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', chosen_email):
        return jsonify({'text': 'This email is in right format',
                        'code': 0})
    else:
        return jsonify({'text': 'Please write email in format: example@domain.com',
                        'code': 1})
