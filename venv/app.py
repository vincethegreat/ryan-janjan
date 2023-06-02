from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQLdb

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

def connection():
	try:
		conn = MySQLdb.connect(host="localhost",user="root",password="",db="db_acts")
		return conn
	except Exception as e:
		return str(e)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form data
        fname = request.form['first-name']
        mname = request.form['middle-name']
        lname = request.form['last-name']
        email = request.form['email']
        usn   = request.form['usn']
        year  = request.form['year']

        conn = connection()
        cur  = conn.cursor()
        cur.execute("INSERT INTO tbl_user VALUES('{}' ,'{}' ,'{}' ,'{}','{}','{}')".format(fname, mname, lname,email,usn,year))
        conn.commit()
        # Save data to a database or perform necessary actions
        return redirect(url_for('home'))
    
    return render_template('register.html')
@app.route('/skills')
def skills():
    # Fetch skills data from a database or any other source
    skills = [
        {'name': 'Skill 1', 'description': 'Description of Skill 1'},
        {'name': 'Skill 2', 'description': 'Description of Skill 2'},
        {'name': 'Skill 3', 'description': 'Description of Skill 3'}
    ]
    return render_template('skills.html', skills=skills)

@app.route('/admin')
def admin():
	conn = connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM tbl_user")
	data = cur.fetchall()

	return render_template('admin.html', data = data)



#admin view
@app.route('/delete_process/<string:id>/')
def delete_process(id):

	conn = connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM tbl_user WHERE USN_NUMBER = '{}'".format(id))
	conn.commit()
	return redirect(url_for('admin'))



@app.route('/update_process_one/<usn>/')
def update_process_one(usn):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tbl_user WHERE USN_NUMBER = %s", (usn,))
    data = cur.fetchone()
    if data:
        return render_template('updateinfo.html', data=data)
    else:
        return "User not found."



@app.route('/update_process_two', methods=['POST'])
def update_process_two():
    if request.method == "POST":
        fname = request.form['first-name']
        mname = request.form['middle-name']
        lname = request.form['last-name']
        email = request.form['email']
        usn = request.form['usn']
        year = request.form['year']

        conn = connection()
        cur = conn.cursor()
        cur.execute("UPDATE tbl_user SET FIRSTNAME = %s, MIDDLENAME = %s, LASTNAME = %s, EMAIL = %s, YEAR_LEVEL = %s WHERE USN_NUMBER = %s", (fname, mname, lname, email, year, usn))
        conn.commit()
        return redirect(url_for('admin'))




if __name__ == '__main__':
    app.run(debug=True)
