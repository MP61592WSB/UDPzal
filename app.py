from flask import Flask, render_template, request,redirect
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'udpbaza.mysql.database.azure.com'#'localhost'
app.config['MYSQL_USER'] = 'udpadmin@udpbaza'#'root'
app.config['MYSQL_PASSWORD'] = 'Pa$$w0rd'
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_SSL_CA'] ='{ca-cert app.py}'
app.config['MYSQL_SSL_VERIFY_CERT'] = 'true'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        if firstName == "":
            firstName="Gal"
        if lastName == "":
            lastName = "Anonim"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM MyUsers")
    if resultValue > 0:
        details = cur.fetchall()
        return render_template('users.html',details = details)

if __name__ == '__main__':
    app.run(debug = True)
