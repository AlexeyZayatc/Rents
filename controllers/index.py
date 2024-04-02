from app import app
from flask import request, session, redirect, url_for, render_template
from utils import get_db_connection
from models.index_model import get_console_search, create_console, get_company
from jinja2 import Environment, FileSystemLoader

@app.route('/',methods=['get'])
def index():
    conn = get_db_connection()
    if request.values.get("console_id")!=None:
        session["console_id"] = request.values.get("console_id")
    if request.values.get("user_id")!=None:
        session["user_id"] = request.values.get("user_id")
    console_name = request.values.get('console_name') 
    is_not_rented = request.values.get('is_not_rented') 

    df_consoles = get_console_search(conn,console_name,is_not_rented)
        
    html = render_template(
        "index.html",
        consoles=df_consoles,
        isNotRented=is_not_rented,
        consoleName=console_name,
        companies = get_company(conn),
        url_for = url_for,
        len=len
    )
    return html

@app.route('/', methods=['post'])
def index_post():
    conn = get_db_connection()
    console_name = request.values.get("new_console_name")
    console_company = request.args.get("new_console_company")
    create_console(conn,console_name,console_company)
    return redirect(url_for("index"))