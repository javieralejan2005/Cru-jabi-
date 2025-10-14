from modelo.clientedao import ClienteDAO

def main():

    #productodao = ProductoDAO()
    #productodao.listarProductos()

    clientedao = ClienteDAO()

    clientedao.cliente.nombre="Diego"
    clientedao.cliente.apellido="Prudente"
    clientedao.cliente.correo_electronico="diego@hotmail.com"
    clientedao.cliente.direccion="lomas de gran jardin"
    clientedao.cliente.telefono="4771457384"
    clientedao.cliente.fecha_registro="2025/10/14"

    #clientedao.guardarCliente()
    #clientedao.listarClientes()
    #clientedao.buscarClientes("julio")
    clientedao.eliminarCliente("Diego")





  

if __name__ == "__main__":

    main()