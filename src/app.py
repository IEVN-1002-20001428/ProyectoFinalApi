import base64
from flask import Flask, jsonify, request, send_from_directory
from flask_mysqldb import MySQL
from config import config
from datetime import datetime
import os

app = Flask(__name__)
con = MySQL(app)
#region Usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * From usuarios'
        cursor.execute(sql)
        datos = cursor.fetchall()
        list_usuarios=[]
        for fila in datos:
            usuario = {
                'nombre':fila[0],
                'correo':fila[1],
                'rol':fila[3]
            }
            list_usuarios.append(usuario)
        return jsonify(list_usuarios)
    except Exception as ex:
        return jsonify({'mensaje':'mamo usuarios'})

def usuarios_bd(nombre, password):
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM usuarios WHERE nombre = "{0}" AND contrasenia = "{1}"'.format(nombre, password)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            usuario = {
                'nombre': datos[0],
                'correo': datos[1],
                'rol': datos[3]
            }
            return usuario
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

def usuario_bd_id(usuario):
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM usuarios WHERE nombre = "{0}"'.format(usuario)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            usuario = {
                'nombre': datos[0],
                'correo': datos[1],
                'contrasenia': datos[2],
                'rol': datos[3]
            }
            return usuario
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/usuarios/<nombre>/<password>', methods=['GET'])
def leer_usuario(nombre, password):
    try:
        usuario=usuarios_bd(nombre, password)
        if usuario != None:
            return jsonify({'usuario':usuario,
                            'mensaje':'Usuario encontrado',
                            'exito': True
                        })
        else:
            return jsonify({'usuario': '','mensaje':'Usuario no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'usuario': '','mensaje':'Error de conexión {}'.format(ex), 'exito': False})

@app.route('/usuarios/<usuario>', methods=['GET'])
def leer_usuario_id(usuario):
    try:
        usuario=usuario_bd_id(usuario)
        if usuario != None:
            return jsonify({'usuario':usuario,
                            'mensaje':'Usuario encontrado',
                            'exito': True
                        })
        else:
            return jsonify({'usuario': '','mensaje':'Usuario no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'usuario': '','mensaje':'Error de conexión {}'.format(ex), 'exito': False})


@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        usuario=usuarios_bd(request.json['correo'], request.json['contrasenia'])
        if usuario != None:
            return jsonify({'mensaje':'Usuario ya existente'})
        else:
            cursor=con.connection.cursor()
            sql="""INSERT INTO usuarios(nombre,correo,contrasenia,rol)
            VALUES  ('{0}','{1}','{2}',1)""".format(request.json['nombre'],
                                                    request.json['correo'],
                                                    request.json['contrasenia'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'usuario': '', 'mensaje':'Usuario ha sido registrado exitosamente', 'exito': True})
    except Exception as ex:
        return jsonify({'usuario': '', 'mensaje':'Mamo la conexión {}'.format(ex), 'exito': False})

@app.route('/usuarios/<user>', methods=['PUT'])
def modificar_usuario(user):
    try:
        usuario = usuario_bd_id(user)
        if usuario is not None:
            nuevo_nombre = request.json.get('usuario')  # Utiliza get para obtener el valor o None si no está presente
            if nuevo_nombre is not None:
                cursor = con.connection.cursor()
                sql = """UPDATE usuarios SET nombre = '{0}', correo = '{1}', contrasenia = '{2}' WHERE nombre = '{0}'""".format(
                    request.json['usuario'],
                    request.json['correo'],
                    request.json['contrasenia']
                )
                cursor.execute(sql)
                con.connection.commit()
                return jsonify({'mensaje': 'Usuario modificado', 'exito': True})
            else:
                return jsonify({'mensaje': 'El campo "nombre" no está presente en la solicitud JSON', 'exito': False})
        else:
            return jsonify({'mensaje': 'Usuario no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/usuarios/<user>', methods=['DELETE'])
def eliminar_usuario(user):
    try:
        usuario = usuario_bd_id(user)
        if usuario != None:
            cursor=con.connection.cursor()
            sql="""DELETE FROM usuarios WHERE nombre = '{0}'""".format(user)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Usuario eliminado', 'exito': True})
        else:
            return jsonify({'mensaje':'Usuario no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje':'Error en la conexión {}'.format(ex), 'exito': False})
#endregion



#region Clientes
@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM clientes'
        cursor.execute(sql)
        datos = cursor.fetchall()
        list_clientes=[]
        for fila in datos:
            cliente = {
                'id_cliente':fila[5],
                'nombre':fila[0],
                'usuario':fila[1],
                'contrasenia':fila[2],
                'correo':fila[3],
                'direccion':fila[4]
            }
            list_clientes.append(cliente)

        return jsonify(list_clientes)
    except Exception as ex:
        return jsonify({'mensaje':'mamo clientes'})

def clientes_bd(usuario, password):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM clientes WHERE usuario = '{0}' AND contrasenia = '{1}'".format(usuario, password)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            cliente = {
                'nombre':datos[0],
                'correo':datos[3],
                'direccion':datos[4]
            }
            return cliente
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex)})

@app.route('/clientes/<usuario>/<password>', methods=['GET'])
def leer_cliente(usuario, password):
    try:
        cliente = clientes_bd(usuario, password)
        if cliente != None:
            return jsonify({'cliente':cliente,
                            'mensaje':'Cliente encontrado',
                            'exito': True
                            })
        else:
            return jsonify({'cliente':'','mensaje':'Cliente no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'cliente': '', 'mensaje':'Error de conexión {}'.format(ex), 'exito': False})

def cliente_bd_id(usuario):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM clientes WHERE usuario = '{0}'".format(usuario)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            cliente = {
                'nombre':datos[0],
                'usuario':datos[1],
                'contrasenia':datos[2],
                'correo':datos[3],
                'direccion':datos[4],
                'id_cliente':datos[5],
            }
            return cliente
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex)})

@app.route('/clientes/<usuario>', methods=['GET'])
def leer_cliente_id(usuario):
    try:
        cliente = cliente_bd_id(usuario)
        if cliente != None:
            return jsonify({'cliente':cliente,
                            'mensaje':'Cliente encontrado',
                            'exito': True
                            })
        else:
            return jsonify({'cliente':'','mensaje':'Cliente no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'cliente': '', 'mensaje':'Error de conexión {}'.format(ex), 'exito': False})

@app.route('/clientes', methods=['POST'])
def registrar_cliente():
    try:
        cliente = clientes_bd(request.json['usuario'], request.json['contrasenia'])
        if cliente != None:
            return jsonify({'cliente':'','mensaje':'Este cliente ya existe', 'exito': False})
        else:
            cursor=con.connection.cursor()
            sql="""INSERT INTO clientes (usuario, nom,contrasenia,correo,direccion)
            VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(request.json['usuario'],
                                                       request.json['nombre'],
                                                       request.json['contrasenia'],
                                                       request.json['correo'],
                                                       request.json['direccion'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'cliente':'', 'mensaje':'El cliente ha sido registrado exitoramente', 'exito': True})
    except Exception as ex:
        return jsonify({'cliente':'', 'mensaje':'Mamo la conexión {}'.format(ex), 'exito': False})

@app.route('/clientes/<usuario>',methods=['PUT'])
def modificar_cliente(usuario):
    try:
        clinete = cliente_bd_id(usuario)
        if clinete is not None:
            cursor = con.connection.cursor()
            sql = """UPDATE clientes SET usuario = '{0}', nom = '{1}', correo = '{2}', direccion = '{3}', contrasenia = '{4}' WHERE usuario = '{0}'""".format(
                usuario,
                request.json['nombre'],
                request.json['correo'],
                request.json['direccion'],
                request.json['contrasenia']
            )
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Cliente modificado','exito': True})
        else:
            return jsonify({'mensaje':'Cliente no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex), 'exito': False})

@app.route('/clientes/<usuario>', methods=['DELETE'])
def eliminar_cliente(usuario):
    try:
        cliente = cliente_bd_id(usuario)
        if cliente != None:
            cursor=con.connection.cursor()
            sql="""DELETE FROM clientes WHERE usuario = '{0}'""".format(usuario)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Cliente eliminado', 'exito': True})
        else:
            return jsonify({'mensaje':'Cliente no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'mennsaje':'Error en la conexión {}'.format(ex), 'exito': False})
#endregion



#region Libros
@app.route('/libros', methods=['GET'])
def obtener_libros():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * From libros'
        cursor.execute(sql)
        datos = cursor.fetchall()
        list_libros=[]
        for fila in datos:
            libro = {
                'id_libro':fila[0],
                'nombre':fila[1],
                'descripcion':fila[2],
                'precio':fila[3],
                'autor':fila[4],
                'editorial':fila[5],
                'existencias':fila[6],
                'id_categoria':fila[7],
                'imagen':fila[8]
            }
            list_libros.append(libro)
        return jsonify(list_libros)
    except Exception as ex:
        return jsonify({'mensaje':'mamo libros'})

def libros_bd(id_libro):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM libros WHERE id_libro = {}".format(id_libro)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            libro = {
                'id_libro':datos[0],
                'nombre':datos[1],
                'descripcion':datos[2],
                'precio':datos[3],
                'autor':datos[4],
                'editorial':datos[5],
                'existencias':datos[6],
                'id_categoria':datos[7],
                'imagen':datos[8]
            }
            return libro
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex)})

@app.route('/libros/<id_libro>',methods=['GET'])
def leer_libro(id_libro):
    try:
        libro = libros_bd(id_libro)
        if libro != None:
            return jsonify({'libro':libro,
                            'mensaje':'Libro encontrado'})
        else:
            return jsonify({'mensaje':'Error de conexión {}'.format(ex)})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex)})

@app.route('/libros', methods=['POST'])
def registrar_libros():
    try:
        nombre_imagen = request.json['nombre'] + '.jpg'
        with open(os.path.join('libros', nombre_imagen), 'wb') as f:
            imagen_base64 = request.json['imagen'].split(',')[1]  # Elimina el encabezado "data:image/jpeg;base64,"
            f.write(base64.b64decode(imagen_base64))
        cursor = con.connection.cursor()
        sql = """INSERT INTO libros (nombre,descripcion,precio,autor,editorial,existencias,id_categoria,imagen)
        VALUES ('{0}','{1}',{2},'{3}','{4}',{5},'{6}','{7}')""".format(request.json['nombre'],
                                                                request.json['descripcion'],
                                                                request.json['precio'],
                                                                request.json['autor'],
                                                                request.json['editorial'],
                                                                request.json['existencias'],
                                                                request.json['categoria'],
                                                                nombre_imagen
                                                                )
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'El libro ha sido registrado exitosamente', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje':'Mamo la conexión {}'.format(ex), 'exito': False})

@app.route('/libros/<id_libro>', methods=['PUT'])
def modificar_libro(id_libro):
    try:
        nombre_imagen = request.json['nombre'] + '.jpg'
        if request.json['imagen']:
            with open(os.path.join('libros', nombre_imagen), 'wb') as f:
                imagen_base64 = request.json['imagen'].split(',')[1]  # Elimina el encabezado "data:image/jpeg;base64,"
                f.write(base64.b64decode(imagen_base64))
        cursor = con.connection.cursor()
        sql = """UPDATE libros SET nombre = '{1}',descripcion = '{2}',precio = {3},autor = '{4}',editorial = '{5}',existencias = {6}, id_categoria = '{7}', imagen = '{8}'
        WHERE id_libro = {0}""".format(id_libro,
                                       request.json['nombre'],
                                       request.json['descripcion'],
                                       request.json['precio'],
                                       request.json['autor'],
                                       request.json['editorial'],
                                       request.json['existencias'],
                                       request.json['categoria'],
                                       nombre_imagen)
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'Libro modificado', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex), 'exito': False})

@app.route('/libros/<id_libro>', methods=['DELETE'])
def eliminar_libro(id_libro):
    try:
        libro = libros_bd(id_libro)
        if libro != None:
            cursor=con.connection.cursor()
            sql="""DELETE FROM libros WHERE id_libro = '{0}'""".format(id_libro)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Libro eliminado'})
        else:
            return jsonify({'mensaje':'Libro no encontrado'})
    except Exception as ex:
        return jsonify({'mennsaje':'Error en la conexión {}'.format(ex)})

@app.route('/covers/<path:filename>')
def serve_static(filename):
    return send_from_directory('libros', filename)
#endregion



#region Categoria
@app.route('/categoria', methods=['GET'])
def obtener_categoria():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * From categoria'
        cursor.execute(sql)
        datos = cursor.fetchall()
        list_categoria=[]
        for fila in datos:
            categoria = {
                'id_categoria':fila[0],
                'nombre':fila[1],
            }
            list_categoria.append(categoria)
        return jsonify(categoria)
    except Exception as ex:
        return jsonify({'mensaje':'mamo categoria'})

def categorias_bd(id_categoria):
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM categoria WHERE id_categoria = "{0}"'.format(id_categoria)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            categoria = {
                'id_categoria': datos[0],
                'nombre': datos[1]
            }
            return categoria
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/categoria/<id_categoria>', methods=['GET'])
def leer_categoria(id_categoria):
    try:
        categoria=categorias_bd(id_categoria)
        if categoria != None:
            return jsonify({'categoria':categoria,
                            'mensaje':'Categoria encontrada',
                            })
        else:
            return jsonify({'mensaje':'Categoria no encontrada'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex)})

@app.route('/categoria', methods=['POST'])
def registrar_categoria():
    try:
        categoria=categorias_bd(request.json['id_categoria'])
        if categoria != None:
            return jsonify({'mensaje':'Categoria ya existente'})
        else:
            cursor=con.connection.cursor()
            sql="""INSERT INTO categoria (nombre) VALUES ('{0}')""".format(request.json['nombre'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'La categoria ha sido registrado exitosamente'})
    except Exception as ex:
        return jsonify({'mensaje':'Mamo la conexión {}'.format(ex)})

@app.route('/categoria/<id_categoria>', methods=['PUT'])
def modificar_categoria(id_categoria):
    try:
        categoria = categorias_bd(id_categoria)
        if categoria is not None:
            cursor = con.connection.cursor()
            sql = """UPDATE categoria SET nombre = '{0}' WHERE id_categoria = '{1}'""".format(
                request.json['nombre'],
                id_categoria
            )
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje': 'Categoria modificada'})
        else:
            return jsonify({'mensaje': 'Categoria no encontrada'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/categoria/<id_categoria>', methods=['DELETE'])
def eliminar_categoria(id_categoria):
    try:
        categoria = categorias_bd(id_categoria)
        if categoria != None:
            cursor=con.connection.cursor()
            sql="""DELETE FROM categoria WHERE id_categoria = '{0}'""".format(id_categoria)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Categoria eliminada'})
        else:
            return jsonify({'mensaje':'Categoria no encontrada'})
    except Exception as ex:
        return jsonify({'mensaje':'Error en la conexión {}'.format(ex)})
#endregion



#region Ventas
@app.route('/ventas', methods=['GET'])
def obtener_ventas():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT v.id_venta, c.nom AS cliente, v.total, v.fecha_venta, v.estatus, GROUP_CONCAT(CONCAT("(", vd.cantidad, ") ", l.nombre) SEPARATOR ", ") AS productos FROM ventas v JOIN clientes c ON c.id_cliente = v.id_cliente JOIN venta_detalle vd ON vd.id_venta = v.id_venta JOIN libros l ON l.id_libro = vd.id_libro GROUP BY v.id_venta, c.nom, v.total, v.fecha_venta, v.estatus'
        cursor.execute(sql)
        datos = cursor.fetchall()
        list_ventas=[]
        for fila in datos:
            venta = {
                'id_venta':fila[0],
                'cliente':fila[1],
                'total':fila[2],
                'fecha_venta':fila[3].strftime('%d/%m/%Y'),
                'estatus':fila[4],
                'productos':fila[5]
            }
            list_ventas.append(venta)
        return jsonify(list_ventas)
    except Exception as ex:
        return jsonify({'mensaje':'mamo ventas'})

def ventas_bd(id_venta):
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM ventas WHERE id_venta = "{0}"'.format(id_venta)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            venta = {
                'id_venta': datos[0],
                'id_cliente':datos[1],
                'total':datos[2],
                'fecha_venta':datos[3],
                'estatus':datos[4]
            }
            return venta
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/ventas/<id_venta>', methods=['GET'])
def leer_venta(id_venta):
    try:
        venta=ventas_bd(id_venta)
        if venta != None:
            return jsonify({'venta':venta,
                            'mensaje':'Venta encontrada',
                            })
        else:
            return jsonify({'mensaje':'Venta no encontrada'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex)})

@app.route('/compras/<id_cliente>', methods=['GET'])
def obtener_compras(id_cliente):
    try:
        cursor = con.connection.cursor()
        sql = """SELECT v.id_venta, c.nom AS cliente, v.total, v.fecha_venta, v.estatus, GROUP_CONCAT(CONCAT("(", vd.cantidad, ") ", l.nombre) SEPARATOR ", ") AS productos FROM ventas v JOIN clientes c ON c.id_cliente = v.id_cliente JOIN venta_detalle vd ON vd.id_venta = v.id_venta JOIN libros l ON l.id_libro = vd.id_libro WHERE v.id_cliente = {0} GROUP BY v.id_venta, c.nom, v.total, v.fecha_venta, v.estatus""".format(id_cliente)
        cursor.execute(sql)
        datos = cursor.fetchall()
        list_compras=[]
        for fila in datos:
            compra = {
                'id_venta':fila[0],
                'cliente':fila[1],
                'total':fila[2],
                'fecha_venta':fila[3].strftime('%d/%m/%Y'),
                'estatus':fila[4],
                'productos':fila[5]
            }
            list_compras.append(compra)
        return jsonify(list_compras)
    except Exception as ex:
        return jsonify({'mensaje':'mamo compras'})

@app.route('/ventas', methods=['POST'])
def registrar_venta():
    try:
        cursor=con.connection.cursor()
        sql="""INSERT INTO ventas(id_cliente,total,fecha_venta,estatus)
        VALUES  ({0},{1},CURDATE(),{2})""".format(request.json['id_cliente'],
                                            request.json['total'],
                                            request.json['estatus'])
        cursor.execute(sql)
        con.connection.commit()
        id_venta = cursor.lastrowid
        return jsonify({'id_venta': id_venta, 'mensaje':'Venta ha sido registrado exitosamente', 'exito': True})
    except Exception as ex:
        return jsonify({'id_venta': 0, 'mensaje':'Mamo la conexión {}'.format(ex), 'exito': False})

@app.route('/ventas/<id_venta>', methods=['PUT'])
def modificar_venta(id_venta):
    try:
        venta = ventas_bd(id_venta)
        if venta is not None:
            cursor = con.connection.cursor()
            sql = """UPDATE ventas SET id_cliente = {0}, fecha_venta = '{1}', estatus = {2} WHERE id_venta = '{3}'""".format(
                request.json['id_cliente'],
                request.json['fecha_venta'],
                request.json['estatus'],
                id_venta
            )
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje': 'Venta modificada'})
        else:
            return jsonify({'mensaje': 'Venta no encontrada'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/ventas/<id_venta>', methods=['DELETE'])
def eliminar_venta(id_venta):
    try:
        venta = ventas_bd(id_venta)
        if venta != None:
            cursor=con.connection.cursor()
            sql="""DELETE FROM ventas WHERE id_venta = '{0}'""".format(id_venta)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Venta eliminada'})
        else:
            return jsonify({'mensaje':'Venta no encontrada'})
    except Exception as ex:
        return jsonify({'mensaje':'Error en la conexión {}'.format(ex)})
#endregion



#region Venta detalles
@app.route('/venta_detalle', methods=['GET'])
def obtener_venta_detalles():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * From venta_detalle'
        cursor.execute(sql)
        datos = cursor.fetchall()
        list_detalle=[]
        for fila in datos:
            detalle = {
                'id_ventadetalle':fila[0],
                'id_venta':fila[1],
                'id_libro':fila[2],
                'cantidad':fila[3],
                'precio_unitario':fila[4],
                'total':fila[5]
            }
            list_detalle.append(detalle)
        return jsonify(detalle)
    except Exception as ex:
        return jsonify({'mensaje':'mamo venta detalles'})

def venta_detalle_bd(id_ventadetalle):
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM venta_detalle WHERE correo = "{0}"'.format(id_ventadetalle)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            detalle = {
                'nombre': datos[0],
                'correo': datos[1],
                'rol': datos[3]
            }
            return detalle
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/venta_detalle/<id_ventadetalle>', methods=['GET'])
def leer_venta_detalle(id_ventadetalle):
    try:
        detalle=venta_detalle_bd(id_ventadetalle)
        if detalle != None:
            return jsonify({'venta detalle':detalle,
                            'mensaje':'Venta detalles encontrado',
                            })
        else:
            return jsonify({'mensaje':'Venta detalles no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexión {}'.format(ex)})

@app.route('/venta_detalle', methods=['POST'])
def registrar_venta_detalle():
    try:
        cursor=con.connection.cursor()
        id_venta = request.json['id_venta']
        productos = request.json['productos']
        for producto in productos:
            sql="""INSERT INTO venta_detalle(id_venta,id_libro,cantidad,precio_unitario,total)
            VALUES  ({0},{1},{2},{3},{4})""".format(id_venta,
                                                    producto['id'],
                                                    producto['cantidad'],
                                                    producto['precio'],
                                                    producto['total'])
            cursor.execute(sql)

            sql_existencias = """UPDATE libros SET existencias = existencias - {0} WHERE id_libro = {1}""".format(
                                                    producto['cantidad'],
                                                    producto['id']
                                                )
            cursor.execute(sql_existencias)
        con.connection.commit()
        return jsonify({'mensaje':'Detalle venta ha sido registrado exitosamente', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje':'Mamo la conexión {}'.format(ex), 'exito': False})

@app.route('/venta_detalle/<id_ventadetalle>', methods=['PUT'])
def modificar_venta_detalle(id_ventadetalle):
    try:
        detalle = venta_detalle_bd(id_ventadetalle)
        if detalle is not None:
            cursor = con.connection.cursor()
            sql = """UPDATE venta_detalle SET id_venta = {0}, id_libro = {1} cantidad = {2} precio_unitario = {3} total = {4}   WHERE id_ventadetalle = {5}""".format(
                request.json['id_venta'],
                request.json['id_libro'],
                request.json['cantidad'],
                request.json['precio_unitario'],
                request.json['total'],
                id_ventadetalle
            )
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje': 'Detalle venta modificado'})
        else:
            return jsonify({'mensaje': 'Detalle venta no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error de conexión {}'.format(ex)})

@app.route('/venta_detalle/<id_ventadetalle>', methods=['DELETE'])
def eliminar_venta_detalle(id_ventadetalle):
    try:
        detalle = venta_detalle_bd(id_ventadetalle)
        if detalle != None:
            cursor=con.connection.cursor()
            sql="""DELETE FROM venta_detalle WHERE id_ventadetalle = '{0}'""".format(id_ventadetalle)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Usuario eliminado'})
        else:
            return jsonify({'mensaje':'Usuario no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje':'Error en la conexión {}'.format(ex)})
#endregion



def pagina_no_encontrada(error):
    return '<h1> Página no encontrada... </h1>',404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()
