import pyodbc

class ConexionBd:
    def __init__(self):
        self.conexion = None

    def establecerConexionBD(self):
        try:
            # usar raw string para el backslash en el nombre del servidor
            conn_str = r"DRIVER={SQL Server};SERVER=SALAF008-08\SQLEXPRESS;DATABASE=bdsistema;UID=sa;PWD=Password01"
            self.conexion = pyodbc.connect(conn_str)
            # opcional: self.conexion.autocommit = False
            print("Conexión exitosa!!!")
        except Exception as error:
            print("Error en conexión: " + str(error))
            self.conexion = None

    def cerrarConexionBD(self):
        try:
            if self.conexion:
                self.conexion.close()
                self.conexion = None
        except Exception as e:
            print("Error cerrando conexión:", e)