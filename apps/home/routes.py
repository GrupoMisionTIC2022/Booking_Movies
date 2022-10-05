from apps.home import blueprint
from flask import render_template, request,redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import InfoUser
from flask_login import current_user



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
        
        
@blueprint.route('/')
def route_default():
    return redirect('/index')

@blueprint.route('/index')

def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        if "home/" + template=="home/settings.html":
            return render_template("home/" + template, segment=segment,info=selec_userinf())
        else:
            return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
