from app import app
from flask import request, session, redirect, url_for, render_template
from utils import get_db_connection
from models.rents_model import  get_rent, get_rent_search, get_user, get_console, approve
from jinja2 import Environment, FileSystemLoader

@app.route('/rents',methods=['get'])
def rents():
    conn=get_db_connection()

    if request.values.get("console_id")!=None:
        session["console_id"] = request.values.get("console_id")
    else:
        session["console_id"] = 0
    if request.values.get("user_id")!=None:
        session["user_id"] = request.values.get("user_id")
    else:
        session["user_id"] = 0

    user_name = request.values.get('rents_user_name')
    console_id = request.values.get('rents_console_id')
    only_returned = request.values.get('rents_returned')
    user = get_user(conn,session['user_id'])
    console = get_console(conn,session['console_id'])

    df_rents = get_rent_search(conn,user_name,console_id,only_returned)

    html = render_template(
        'rents.html',
        selected_user=user,
        selected_console=console,
        userName = user_name,
        consoleId=console_id,
        onlyReturned=only_returned,
        rents=df_rents,
        len=len
    )
    return html


@app.route('/rents_post', methods=["post"])
def rents_post():
    conn = get_db_connection()
    rent_user_id = request.values.get('rent_user_id')
    rent_console_id = request.values.get('rent_console_id')
    if rent_user_id==None or rent_console_id==None:
        return redirect(url_for('rents'))
    
    approve(conn, rent_user_id,rent_console_id)
    return redirect(url_for("rents"))