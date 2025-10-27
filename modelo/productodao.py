from modelo.conexionbd import ConexionBd
from modelo.producto import Producto

class ProductoDAO:
    def __init__(self):
        self.bd = ConexionBd()
        self.producto = Producto()

    def listarProductos(self):
        self.bd.establecerConexionBD()
        if not self.bd.conexion:
            return []
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_listar_productos]"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas

    def insertarProducto(self):
        self.bd.establecerConexionBD()
        if not self.bd.conexion:
            return
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_insertar_producto] @clave=?, @descripcion=?, @existencia=?, @precio=?"
        parametros = (
            self.producto.clave,
            self.producto.descripcion,
            self.producto.existencia,
            self.producto.precio,
        )
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()

    def actualizarProducto(self):
        self.bd.establecerConexionBD()
        if not self.bd.conexion:
            return
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_actualizar_producto] @id_producto=?, @clave=?, @descripcion=?, @existencia=?, @precio=?"
        parametros = (
            self.producto.id_producto,
            self.producto.clave,
            self.producto.descripcion,
            self.producto.existencia,
            self.producto.precio,
        )
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()

    def eliminarProducto(self):
        self.bd.establecerConexionBD()
        if not self.bd.conexion:
            return
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_eliminar_producto] @id_producto=?"
        parametros = (self.producto.id_producto,)
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()

    def contarProductos(self):
        self.bd.establecerConexionBD()
        if not self.bd.conexion:
            return None
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_contar_productos]"
        cursor.execute(sp)
        resultado = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return resultado[0] if resultado else None

    def buscarProductos(self):
        self.bd.establecerConexionBD()
        if not self.bd.conexion:
            return []
        cursor = self.bd.conexion.cursor()
        sp = "exec [dbo].[sp_buscar_producto] @clave=?"
        parametros = (self.producto.clave,)
        cursor.execute(sp, parametros)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas