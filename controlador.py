#Importar el módulo flask
from flask import Flask, render_template, request, redirect, url_for, session
#importar MySQL de flask-mysqldb
from flask_mysqldb import MySQL
#Crear un objeto que tome todas las características y métodos de la clase Flask
app = Flask(__name__)
#Clave secreta para la sesión
app.secret_key = '3005'

#Conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost' #servidor
app.config['MYSQL_USER'] = 'root' #usuario
app.config['MYSQL_PASSWORD'] = '' #contraseña
app.config['MYSQL_DB'] = 'tienda_videojuegos' #nombre de la bd

#Crear un objeto para el uso de métodos de bd en python flask
mysql = MySQL(app)

#debug
d = True
#port
p = 8000

#rutas
@app.route('/')
def index():
    return '<p>Hola señores estudiantes</p>'

@app.route('/videojuegos')
def videojuegos():
    #crear un cursor
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM videojuegos')
    #objeto para guardar los resultados que se obtienen de la consulta
    videojuegos = cursor.fetchall()
    #renderizar videojuegos.html y enviar datos de videojuegos en objeto v
    return render_template('videojuegos.html', v = videojuegos)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    #Obtener los datos del formulario (registrarse.html)
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    color = request.form['color']
    rol = request.form['rol']

    if not nombre or not apellido or not usuario or not contrasena or not color or not rol:
        return render_template('registrarse.html', mensaje='Todos los campos son obligatorios')
    #Crear un cursor
    cursor = mysql.connection.cursor()
    #Ejecutar la consulta de inserción
    sqlInsert = 'INSERT INTO usuario (nombre_usuario, apellido_usuario, usuario, contrasena, color, rol) VALUES (%s, %s, %s, %s, %s, %s)'
    datos = (nombre, apellido, usuario, contrasena, color, rol)
    cursor.execute(sqlInsert, datos)
    #Guardar los cambios en la base de datos
    mysql.connection.commit()
    #Cerrar el cursor
    cursor.close()
    #Redireccionar a la página de inicio o a otra página
    return redirect(url_for('videojuegos'))

@app.route('/cargar_usuario', methods=['POST'])
def cargar_usuario():
    #Obtener los datos del formulario (login.html)    
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    #Crear un cursor
    cursor = mysql.connection.cursor()
    sqlSelect = 'SELECT * FROM usuario WHERE usuario = %s AND contrasena = %s'
    usuario_datos = (usuario, contrasena)

    cursor.execute(sqlSelect, usuario_datos)
    usuario_encontrado = cursor.fetchone()
    cursor.close()

    if usuario_encontrado:
        session['usuario'] = usuario_encontrado[4]
        session['color'] = usuario_encontrado[3]
        session['rol'] = usuario_encontrado[6]
        return redirect(url_for('videojuegos'))
    else:
        return render_template('login.html', mensaje='Usuario o contraseña incorrectos')


@app.route('/logout')
def logout():
    #Eliminar la sesión del usuario
    session.pop('usuario', None)
    session.pop('color', None)
    session.pop('rol', None)
    #Redireccionar a la página de inicio o a otra página
    return redirect(url_for('videojuegos'))

@app.route('/editar_perfil')
def editar_perfil():
    #Verificar si el usuario está autenticado
    if 'usuario' in session:
        #Obtener el nombre de usuario de la sesión
        usuario = session['usuario']
        #Crear un cursor
        cursor = mysql.connection.cursor()
        #Consulta para obtener los datos del usuario
        sqlSelect = 'SELECT * FROM usuario WHERE usuario = %s'
        cursor.execute(sqlSelect, (usuario,))
        usuario_datos = cursor.fetchone()
        cursor.close()
        return render_template('actualizar_usuario.html', u=usuario_datos)
    else:
        return redirect(url_for('login'))

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    #Obtener los datos del formulario (editar_perfil.html)
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    color = request.form['color']

    session['usuario'] = usuario  # Actualizar el usuario en la sesión
    session['color'] = color  # Actualizar el color en la sesión

    #Verificar si el usuario está autenticado
    if 'usuario' in session:
        #Crear un cursor
        cursor = mysql.connection.cursor()
        #Consulta para actualizar los datos del usuario
        sqlUpdate = 'UPDATE usuario SET nombre_usuario = %s, apellido_usuario = %s, contrasena = %s, color = %s WHERE usuario = %s'
        datos = (nombre, apellido, contrasena, color, usuario)
        cursor.execute(sqlUpdate, datos)
        #Guardar los cambios en la base de datos
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('videojuegos'))
    else:
        return redirect(url_for('login'))

@app.route('/videojuego/<int:id>')
def videojuego(id):
    #Crear un cursor
    cursor = mysql.connection.cursor()
    #Consulta para obtener los datos del videojuego por su ID
    sqlVideojuego = 'SELECT * FROM videojuegos WHERE id_videojuego = %s'
    cursor.execute(sqlVideojuego, (id,))
    videojuego = cursor.fetchone()
    #Consulta para obtener los datos del videojuego por su ID    
    sqlDetalleVideojuego = 'SELECT * FROM detalle_videojuego WHERE id_videojuego = %s'
    cursor.execute(sqlDetalleVideojuego, (id,))
    detalle_videojuego = cursor.fetchone()
    cursor.close()
    return render_template('detalle_videojuego.html', dv=detalle_videojuego, v=videojuego)

@app.route('/videojuegos/crear')
def crearVideojuego():
    #Verificar si el usuario es administrador
    if 'rol' in session and session['rol'] == 'admin':
        return render_template('crear_videojuego.html')
    else:
        return redirect(url_for('videojuegos'))

@app.route('/crear_videojuego', methods=['POST'])
def crear_videojuego():
    #Obtener los datos del formulario (crear_videojuego.html)
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = request.form['precio']
    sinopsis = request.form['sinopsis']
    plataforma = request.form['plataforma']
    imagen = request.files['imagen']
    otras_plataformas = request.form['otras_plataformas']
    desarrollador = request.form['desarrollador']
    fecha_lanzamiento = request.form['fecha_lanzamiento']

    nombre_imagen = imagen.filename
    #Guardar la imagen en la carpeta 'static/imagenes/'
    imagen.save(f'static/imagenes/{nombre_imagen}')

    #Crear un cursor
    cursor = mysql.connection.cursor()
    #Consulta para insertar el videojuego
    sqlInsertVideojuego = 'INSERT INTO videojuegos (nombre_videojuego, categoria, precio, imagen, plataforma) VALUES (%s, %s, %s, %s, %s)'
    datosVideojuego = (nombre, categoria, precio, nombre_imagen, plataforma)
    cursor.execute(sqlInsertVideojuego, datosVideojuego)
    #Consulta para insertar los detalles del videojuego

    #Usar LAST_INSERT_ID() para obtener el último ID insertado en la tabla videojuegos
    sqlInsertDetalle = 'INSERT INTO detalle_videojuego (id_videojuego, sinopsis, desarrollador, otras_plataformas, fecha_lanzamiento) VALUES (LAST_INSERT_ID(), %s, %s, %s, %s)'
    datosDetalle = (sinopsis, desarrollador, otras_plataformas, fecha_lanzamiento)
    cursor.execute(sqlInsertDetalle, datosDetalle)
    #Guardar los cambios en la base de datos
    mysql.connection.commit()
    cursor.close()
    
    return redirect(url_for('videojuegos'))

@app.route('/actualizar_videojuego/<int:id>')
def actualizar_videojuego(id):
    #Verificar si el usuario es administrador
    if 'rol' in session and session['rol'] == 'admin':
        #Crear un cursor
        cursor = mysql.connection.cursor()
        #Consulta para obtener los datos del videojuego por su ID
        sqlVideojuego = 'SELECT * FROM videojuegos WHERE id_videojuego = %s'
        cursor.execute(sqlVideojuego, (id,))
        videojuego = cursor.fetchone()
        #Consulta para obtener los detalles del videojuego por su ID
        sqlDetalleVideojuego = 'SELECT * FROM detalle_videojuego WHERE id_videojuego = %s'
        cursor.execute(sqlDetalleVideojuego, (id,))
        detalle_videojuego = cursor.fetchone()
        cursor.close()
        return render_template('actualizar_videojuego.html', v=videojuego, dv=detalle_videojuego)
    else:
        return redirect(url_for('videojuegos'))
    
@app.route('/guardar_actualizacion_videojuego/<int:id>', methods=['POST'])
def guardar_actualizacion_videojuego(id):
    #Obtener los datos del formulario (actualizar_videojuego.html)
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = request.form['precio']
    sinopsis = request.form['sinopsis']
    plataforma = request.form['plataforma']
    imagen = request.files['imagen']
    otras_plataformas = request.form['otras_plataformas']
    desarrollador = request.form['desarrollador']
    fecha_lanzamiento = request.form['fecha_lanzamiento']

    if imagen:
        nombre_imagen = imagen.filename
        #Guardar la imagen en la carpeta 'static/imagenes/'
        imagen.save(f'static/imagenes/{nombre_imagen}')
    else:
        nombre_imagen = None

    #Crear un cursor
    cursor = mysql.connection.cursor()
    
    #Actualizar el videojuego
    sqlUpdateVideojuego = 'UPDATE videojuegos SET nombre_videojuego = %s, categoria = %s, precio = %s, plataforma = %s' + (', imagen = %s' if nombre_imagen else '') + ' WHERE id_videojuego = %s'
    datosVideojuego = (nombre, categoria, precio, plataforma, id)
    
    if nombre_imagen:
        datosVideojuego += (nombre_imagen,)
    
    cursor.execute(sqlUpdateVideojuego, datosVideojuego)
    
    #Actualizar los detalles del videojuego
    sqlUpdateDetalle = 'UPDATE detalle_videojuego SET sinopsis = %s, desarrollador = %s, otras_plataformas = %s, fecha_lanzamiento = %s WHERE id_videojuego = %s'
    datosDetalle = (sinopsis, desarrollador, otras_plataformas, fecha_lanzamiento, id)
    
    cursor.execute(sqlUpdateDetalle, datosDetalle)
    
    #Guardar los cambios en la base de datos
    mysql.connection.commit()
    cursor.close()
    
    return redirect(url_for('videojuegos'))

@app.route('/eliminar_videojuego/<int:id>')
def eliminar_videojuego(id):
    #Verificar si el usuario es administrador
    if 'rol' in session and session['rol'] == 'admin':
        #Crear un cursor
        cursor = mysql.connection.cursor()
        #Consulta para eliminar los detalles del videojuego por su ID
        sqlDeleteDetalle = 'DELETE FROM detalle_videojuego WHERE id_videojuego = %s'
        cursor.execute(sqlDeleteDetalle, (id,))
        #Consulta para eliminar el videojuego por su ID
        sqlDeleteVideojuego = 'DELETE FROM videojuegos WHERE id_videojuego = %s'
        cursor.execute(sqlDeleteVideojuego, (id,))
        #Guardar los cambios en la base de datos
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('videojuegos'))
    else:
        return redirect(url_for('videojuegos'))

#Correr la app
if __name__ == '__main__':
    app.run(debug = d, port = p)