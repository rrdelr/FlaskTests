from flask import Blueprint, render_template
from utils.utils import plotrose

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route('/')
def index():
    polar = plotrose()
    return render_template('index.html', plot = polar)

