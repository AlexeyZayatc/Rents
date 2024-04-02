from app import app
from flask import request, session, redirect, url_for, render_template
from utils import get_db_connection
from models.return_rent_model import get_user, get_console, db_return_rent

@app.route('/return_rent', methods=["get"])
def return_rent():
    conn=get_db_connection()
    # выводим форму
    user = get_user(conn,session['user_id'])
    console = get_console(conn,session['console_id'])
    return render_template(
        'return_rent.html',
        selected_user=user,
        selected_console=console,
        rent_return_id=request.values.get('rent_return_id')
    )

@app.route('/return_rent', methods=["post"])
def return_rent_post():
    conn = get_db_connection()
    rent_id = request.values.get('rent_return_id')
    penalty = request.values.get('penalty')
    if penalty==None or penalty=='':
        penalty=0
    penalty=int(penalty)
    db_return_rent(conn,rent_id,penalty)
    return redirect(url_for("rents"))