# se importan las librerias a usar
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 

app = Flask(__name__)

# coneccion MySQL - BD en la nube
app.config['MYSQL_HOST'] = 'budspoj4ww8wk7op94bh-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uamnk30mtvpy7ga2'
app.config['MYSQL_PASSWORD'] = 'DeRiQKldlgFk0iL5kTNJ'
app.config['MYSQL_DB'] = 'budspoj4ww8wk7op94bh'
mysql = MySQL(app)

#config
app.secret_key ='mysecretkey'

# decodador para homepage
@app.route('/') 
def Index():
    cur = mysql.connection.cursor() # se establece la conexion con la bd
    cur.execute('SELECT * FROM contactos') 
    data = cur.fetchall() # se obtiene una tupla de contactos mediante la query
    return render_template('index.html', contacts = data) # se muestra la plantilla html con la data

# decodador para pagina de agregar contacto
@app.route('/add_contact', methods=['POST']) 
def add_contact():
    if request.method == 'POST':
        # se obtienen los datos del form
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        # se genera un puntero a la bd
        cur = mysql.connection.cursor()
        # se ejecuta la query de insercion de data
        cur.execute('INSERT INTO contactos(nombreContacto, telefono, correo) VALUES (%s, %s, %s)',
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto agregado!') # mensaje en respuesta
        return redirect(url_for('Index')) # redireccion a la pagina index

# decodador para pagina de editar contacto
@app.route ('/edit/<id>')
def get_contact(id):
    # se genera un puntero a la bd
    cur = mysql.connection.cursor()
    # se ejecuta la query que obtendra los datos del registro a modificar
    cur.execute('SELECT * FROM contactos WHERE id = %s', (id))
    data = cur.fetchall() # se obtiene una tupla de la data
    return render_template('edit-contact.html', contact = data[0]) # se muestra la plantilla html edit-contact con la data solicitada

# decodador para pagina de actualizar contacto
@app.route('/update/<id>', methods = ['POST'])
def update_contac(id):
    if request.method == 'POST':
        # se obtienen los datos del form de modificacion de datos
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        # se genera un puntero a la bd
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contactos
            SET nombreContacto = %s,
                telefono = %s,
                correo = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit() # se ejecuta la query
        flash('Contacto actualizado adecuadamente') # mensaje respuesta
        return redirect(url_for('Index')) # redireccion a la pagina index

# decodador para pagina de eliminar contacto
@app.route ('/delete/<string:id>')
def delete_contact(id):
    # se genera un puntero a la bd
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit() # se ejecuta la query
    flash('Se ha eliminado el contacto') # mensaje respuesta
    return redirect(url_for('Index')) # redireccion a la pagina index

# funcion principal
if __name__ == '__main__':
    app.run(port = 3000, debug = True) # puerto de ejecucion y debug activado