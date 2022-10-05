
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from apps.authentication.util import hash_pass
from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users,InfoUser

from apps.authentication.util import verify_pass




# Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect('/tabla_pelis.html')

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Sabemos que te encanta ese nombre de usuario pero ya existe.',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='El correo electrónico ya ha sido registrado registrado',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/infouser', methods=['GET', 'POST'])
def submitinfouser():
    username      = str(current_user.username)
    first_name    = str(request.form["first_name"])
    last_name     = str(request.form["last_name"])
    birthday      = str(request.form["birthday"])
    gender        = str(request.form["gender"])
    email         = str(request.form["email"])
    phone         = int(request.form["phone"])

    cond=InfoUser.query.filter_by(username=username).first() 
    if cond:
        id=cond.id
        info=InfoUser(id=id,username=username,
                  frist_name=first_name,
                  last_name=last_name,
                  birthday=birthday,
                  gender=gender,
                  email=email,
                  phone=phone)
        db.session.add(info)
    else:     
        cond.frist_name=first_name
        cond.last_name=last_name
        cond.birthday=birthday
        cond.gender=gender
        cond.email=email
        cond.phone=phone
    
    db.session.commit()
    return  redirect("/tabla_pelis.html")
    
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/moduser', methods=['GET', 'POST'])
def submitmoduser():
    username = request.form['username']
    user = Users.query.filter_by(username=current_user.username).first()
    user.username=username
    db.session.commit()
    return redirect("/settings.html")

@blueprint.route('/modpassword', methods=['GET', 'POST'])
def submitmodpass():
    password = request.form['password']
    user = Users.query.filter_by(username=current_user.username).first()
    user.password=hash_pass(password)
    db.session.commit()
    return redirect("/settings.html")
# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

def selec_userinf():
    user = InfoUser.query.filter_by(username=current_user.username).first()
    if user:
        return user
    else:
        user={}
        user["frist_name"]=current_user.username
        user["last_name"]=""
        user["birthday"]=""
        user["gender"]=""
        user["email"]=""
        user["phone"]=""
        return user
        
        
