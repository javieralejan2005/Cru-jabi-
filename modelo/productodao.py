from modelo.conexionbd import ConexionBd
from modelo.producto import Producto 


class ProductoDAO:


    def __init__(self):

        self.bd = ConexionBd()
        self.producto = Producto()

    def listarProductos(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_listar_productos]"
        cursor.execute(sp)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas

    def insertarProducto(self):

        # Abrir la conexión a la base de datos  

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_insertar_producto] @clave=?, @descripcion=?, @existencia=?, @precio=?"
        parametros = (self.producto.clave, self.producto.descripcion, self.producto.existencia, self.producto.precio)
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        # Cerrar la conexión a la base de datos

        self.bd.cerrarConexionBD()

    def actualizarProducto(self):

        # Abrir la conexión a la base de datos  

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_actualizar_producto] @idProducto=?, @clave=?, @descripción=?, @existencia?, @precio=?"
        parametros = (self.producto.idProducto, self.producto.clave, self.producto.descripcion, self.producto.existencia, self.producto.precio)
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        # Cerrar la conexión a la base de datos

        self.bd.cerrarConexionBD()

    def eliminarProducto(self):

        # Abrir la conexión a la base de datos  

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_eliminar_producto] @idProducto=?"
        parametros = (self.producto.idProducto)
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        # Cerrar la conexión a la base de datos

        self.bd.cerrarConexionBD()

    
    def contarProductos(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_contar_productos]"
        cursor.execute(sp)
        resultado = cursor.fetchone()

        print(f"Total de productos: {resultado[0]}")

        self.bd.cerrarConexionBD()

    def buscarProductos(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_buscar_producto] @clave =?"
        param = [self.producto.clave]
        cursor.execute(sp, param)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas


