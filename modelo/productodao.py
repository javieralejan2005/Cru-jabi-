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

        for fila in filas:
            print(fila)

        self.bd.cerrarConexionBD()


