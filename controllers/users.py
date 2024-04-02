from app import app
from flask import request, session, redirect, url_for, render_template
from utils import get_db_connection
from models.users_model import get_user, get_user_search, create_user
from jinja2 import Environment, FileSystemLoader

@app.route('/users',methods=['get'])
def users():
    conn = get_db_connection()
    
    if request.values.get("console_id")!=None:
        session["console_id"] = request.values.get("console_id")
    if request.values.get("user_id")!=None:
        session["user_id"] = request.values.get("user_id")

    user_name=request.values.get('user_name')
    has_rented=request.values.get('has_rented')
    usrs = get_user_search(conn,user_name,has_rented)  
        
    html = render_template(
        "users.html",
        hasRented=has_rented,
        userName=user_name,
        users=usrs,
        len=len
    )
    return html

@app.route('/users', methods=['post'])
def users_post():
    conn = get_db_connection()
    user_name = request.values.get("new_user_name")
    phone_number = request.values.get("new_phone_number")
    inserted_id = create_user(conn, user_name,phone_number)
    session["user_id"] = inserted_id
    return redirect(url_for("users"))