from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QStackedWidget, QTableWidgetItem
import sys
import os
import traceback

PROJECT_DIR = os.path.dirname(__file__)
UI_LOGIN = os.path.join(PROJECT_DIR, "ui", "ui_iniciarsesion.ui")
UI_PRODUCTOS = os.path.join(PROJECT_DIR, "ui", "ui_productos.ui")
UI_CLIENTES = os.path.join(PROJECT_DIR, "ui", "clientes_ui.ui")

def safe_load_ui(path, widget):
    try:
        uic.loadUi(path, widget)
    except Exception:
        print(f"Error cargando {path}")
        traceback.print_exc()
        raise

class ClientWindow(QMainWindow):
    def __init__(self, style_source=None):
        super().__init__()
        safe_load_ui(UI_CLIENTES, self)
        self.setWindowTitle("Catálogo de Clientes")

        # stacked widget en clientes_ui.ui se llama stackedWidget_2
        self.sw = getattr(self, "stackedWidget_2", None) or self.findChild(QStackedWidget)

        # mapping botón lateral -> nombre de página del .ui
        page_names = {
            "boton_crear": "page_crear",
            "boton_buscar": "page_buscar",
            "boton_editar": "page_editar",
            "boton_listar": "page_listar",
            "boton_eliminar": "page_eliminar",
        }

        def index_of_page(name, fallback=None):
            if not self.sw:
                return None
            for i in range(self.sw.count()):
                w = self.sw.widget(i)
                try:
                    if w.objectName() == name:
                        return i
                except Exception:
                    continue
            if fallback is not None and 0 <= fallback < self.sw.count():
                return fallback
            return None

        # fallback indices basados en el orden del .ui
        fallback_indices = {
            "page_crear": 0,
            "page_buscar": 1,
            "page_editar": 2,
            "page_listar": 4,
            "page_eliminar": 5,
        }

        if self.sw:
            for btn_name, page_name in page_names.items():
                idx = index_of_page(page_name, fallback_indices.get(page_name))
                if idx is None:
                    continue
                btn = getattr(self, btn_name, None) or self.findChild(QPushButton, btn_name)
                if btn:
                    btn.clicked.connect(lambda _, i=idx: self.sw.setCurrentIndex(i))

        # conectar botón listar/refrescar para cargar tabla (si existe)
        refrescar = getattr(self, "boton_accion_refrescar", None) or self.findChild(QPushButton, "boton_accion_refrescar")
        if refrescar:
            refrescar.clicked.connect(self.load_clients_table)

        # copiar stylesheet desde style_source o aplicación
        try:
            if style_source is not None and getattr(style_source, "styleSheet", None):
                ss = style_source.styleSheet()
                if ss:
                    self.setStyleSheet(ss)
            else:
                app = QApplication.instance()
                if app and app.styleSheet():
                    self.setStyleSheet(app.styleSheet())
        except Exception:
            pass

        # conectar salir si existe
        app = QApplication.instance()
        salir = getattr(self, "boton_salir", None) or self.findChild(QPushButton, "boton_salir")
        if salir:
            try:
                salir.clicked.connect(app.quit)
            except Exception:
                pass

    def load_clients_table(self):
        # Carga mínima: limpiar tabla y mostrar cabeceras (no tocar .ui)
        tabla = getattr(self, "tabla_clientes", None) or self.findChild(type(getattr(self, "tabla_clientes", None)), "tabla_clientes")
        if tabla is None:
            tabla = self.findChild(type(QTableWidgetItem()), "tabla_clientes")
        try:
            tabla = getattr(self, "tabla_clientes", None) or self.findChild(type(tabla), "tabla_clientes")
        except Exception:
            tabla = getattr(self, "tabla_clientes", None)
        if tabla is None:
            return
        # ejemplo: borrar filas actuales
        try:
            tabla.setRowCount(0)
        except Exception:
            pass
        # aquí puedes cargar datos desde ClienteDAO y agregarlos:
        # rows = ClienteDAO().listarClientes()
        # for r in rows: ...
        # Dejo la tabla vacía para no cambiar la estructura de la UI.

class ProductWindow(QMainWindow):
    def __init__(self, style_source=None):
        super().__init__()
        safe_load_ui(UI_PRODUCTOS, self)
        self.setWindowTitle("Catálogo de Productos")

        # stacked widget en productos
        self.sw = getattr(self, "stackedWidget", None) or self.findChild(QStackedWidget)

        page_names = {
            "boton_agregar": "page_agregar",
            "boton_buscar": "page_buscar",
            "boton_actualizar": "page_actualizar",
            "boton_eliminar": "page_eliminar",
            "boton_consultar": "page_consultar",
        }

        def index_of_page(name, fallback=None):
            if not self.sw:
                return None
            for i in range(self.sw.count()):
                w = self.sw.widget(i)
                try:
                    if w.objectName() == name:
                        return i
                except Exception:
                    continue
            if fallback is not None and 0 <= fallback < self.sw.count():
                return fallback
            return None

        fallback_indices = {
            "page_agregar": 0,
            "page_buscar": 1,
            "page_actualizar": 2,
            "page_consultar": 3,
            "page_eliminar": 4,
        }

        if self.sw:
            for btn_name, page_name in page_names.items():
                idx = index_of_page(page_name, fallback_indices.get(page_name))
                if idx is None:
                    continue
                btn = getattr(self, btn_name, None) or self.findChild(QPushButton, btn_name)
                if btn:
                    btn.clicked.connect(lambda _, i=idx: self.sw.setCurrentIndex(i))

        try:
            if style_source is not None and getattr(style_source, "styleSheet", None):
                ss = style_source.styleSheet()
                if ss:
                    self.setStyleSheet(ss)
            else:
                app = QApplication.instance()
                if app and app.styleSheet():
                    self.setStyleSheet(app.styleSheet())
        except Exception:
            pass

        app = QApplication.instance()
        salir = getattr(self, "boton_salir", None) or getattr(self, "pushButton_2", None) or self.findChild(QPushButton, "boton_salir")
        if salir:
            try:
                salir.clicked.connect(app.quit)
            except Exception:
                pass

class SelectionWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        safe_load_ui(UI_LOGIN, self)
        self.setWindowTitle("Seleccionar catálogo")
        try:
            self.stackedWidget.setCurrentIndex(1)
        except Exception:
            pass

        # conectar botones de selección (clientes/productos)
        btn_clients = getattr(self, "pushButton_3", None) or self.findChild(QPushButton, "pushButton_3")
        if btn_clients:
            btn_clients.clicked.connect(self.open_clients_catalog)
        btn_products = getattr(self, "pushButton_4", None) or self.findChild(QPushButton, "pushButton_4")
        if btn_products:
            btn_products.clicked.connect(self.open_products_catalog)

    def open_clients_catalog(self):
        if not os.path.exists(UI_CLIENTES):
            QMessageBox.critical(self, "Error", f"No se encontró {UI_CLIENTES}")
            return
        try:
            cw = ClientWindow(style_source=self)
        except Exception:
            QMessageBox.critical(self, "Error", "No se pudo abrir el catálogo de clientes. Revisa la terminal.")
            return
        app = QApplication.instance()
        setattr(app, "client_window", cw)  # guardar referencia para evitar GC
        cw.show()
        self.close()

    def open_products_catalog(self):
        if not os.path.exists(UI_PRODUCTOS):
            QMessageBox.critical(self, "Error", f"No se encontró {UI_PRODUCTOS}")
            return
        try:
            pw = ProductWindow(style_source=self)
        except Exception:
            QMessageBox.critical(self, "Error", "No se pudo abrir el catálogo de productos. Revisa la terminal.")
            return
        app = QApplication.instance()
        setattr(app, "product_window", pw)
        pw.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        safe_load_ui(UI_LOGIN, self)
        self.setWindowTitle("Iniciar sesión")
        try:
            self.stackedWidget.setCurrentIndex(0)
        except Exception:
            pass

        btn_login = getattr(self, "pushButton", None) or self.findChild(QPushButton, "pushButton")
        if btn_login:
            btn_login.clicked.connect(self.on_login)
        btn_exit = getattr(self, "pushButton_2", None) or self.findChild(QPushButton, "pushButton_2")
        if btn_exit:
            btn_exit.clicked.connect(QApplication.instance().quit)

        self.selection_window = None

    def on_login(self):
        usuario = getattr(self, "lineEdit", None)
        clave = getattr(self, "lineEdit_2", None)
        user_text = usuario.text() if usuario else ""
        pass_text = clave.text() if clave else ""
        if not user_text or not pass_text:
            QMessageBox.warning(self, "Error", "Ingrese usuario y contraseña")
            return
        self.selection_window = SelectionWindow(parent=self)
        self.selection_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())