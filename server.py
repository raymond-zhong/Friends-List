from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)
@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/update_friend', methods=['POST'])
def update_button():
    friendid = request.form['modify']
    query = "SELECT * FROM friends WHERE id = '{id}'".format(id=friendid)
    friends = mysql.query_db(query)
    return render_template('update.html', friendid1=friendid, all_friends=friends)
@app.route('/friends/<friend_id>', methods=['POST'])
def update(friend_id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation'],
             'id': friend_id
           }
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/friends/confirm/<friend_id>', methods=['POST'])
def confirm_button(friend_id):
    friendid = friend_id
    query = "SELECT * FROM friends WHERE id = '{id}'".format(id=friendid)
    friends = mysql.query_db(query)
    return render_template('confirm.html',friend_id = friend_id, all_friends=friends)
@app.route('/remove_friend/<friend_id>', methods=['POST'])
def delete(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/home', methods=['POST'])
def home():
    return redirect('/')
app.run(debug=True)
