from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 

app = Flask(__name__)

# Coneccion MySQL
app.config['MYSQL_HOST'] = 'budspoj4ww8wk7op94bh-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uamnk30mtvpy7ga2'
app.config['MYSQL_PASSWORD'] = 'DeRiQKldlgFk0iL5kTNJ'
app.config['MYSQL_DB'] = 'budspoj4ww8wk7op94bh'
mysql = MySQL(app)

#Config
app.secret_key ='mysecretkey'

# Decodador
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos') # se obtiene una tupla de contactos
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos(nombreContacto, telefono, correo) VALUES (%s, %s, %s)',
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto agregado!')
        return redirect(url_for('Index'))

@app.route ('/edit')
def edit_contact():
    return 'edit contact'
    # 48:29 min

@app.route ('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Se ha eliminado el contacto')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)