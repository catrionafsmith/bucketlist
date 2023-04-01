# Issues:
# Code for creating mysql connector and cursor needs to be inside a try block in the signUp() function- see GitHub
# Remove the 'Finally' section after that try/except block. cursor will be closed automatically
# importing MySQL from flask.ext.mysql -> need to do: flask_mysql or flaskext.mysql
# importing generate_password_hash -> Need to import it from werkzeug.security instead. Also this caused an error, so I just took it out entirely
# Make sure to add own details in the MySQL configuration section
# Could add debug=True to app.run, so that this page is updated automatically
# When creating the table in MYSQL, you need to note that the user_id should be NOT_NULL, and then asd the link UNIQUE ( `user_username` ) at the end, after the PRIMARY_KEY
# Also, in the stored procedure, for some reason they have makde the name, username and password only 40 characters, when it was 80 in the original table.
# Ongoing problem that if I try to enter a password longer than 20 characters then I get the error message: {error: `(1406, "Data too long for column 'p_username' at row 1")`}
# Needed to edit and save the stored procedure (created a new one called 'sp_createUser2' to fix this issue.)


from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'INSERT_YOUR_MYSQL_PASSWORD_HERE'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/api/signup', methods=['POST'])
def signUp():
#     Create user code will be here
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

    #     Validate the received values
        if _name and _email and _password:

            # If it is all good, then call the MySQL stored proc
            conn = mysql.connect()
            cursor = conn.cursor()
            # _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser2', (_name, _email, _password)) #was _hashed_password in here
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully!'})
            else:
                return json.dumps({'error': str(data[0])})

        else:
            return json.dumps({'html': '<span>Enter the required info pls</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run()