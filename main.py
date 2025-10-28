from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QStackedWidget
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

        self.sw = getattr(self, "stackedWidget_2", None) or self.findChild(QStackedWidget)

        page_map = {
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
                if getattr(w, "objectName", lambda: None)() == name:
                    return i
            if fallback is not None and 0 <= fallback < self.sw.count():
                return fallback
            return None

        fallback_indices = {
            "page_crear": 0,
            "page_buscar": 1,
            "page_editar": 2,
            "page_listar": 4,
            "page_eliminar": 5,
        }

        if self.sw:
            for btn_name, page_name in page_map.items():
                idx = index_of_page(page_name, fallback_indices.get(page_name))
                if idx is None:
                    continue
                btn = getattr(self, btn_name, None) or self.findChild(QPushButton, btn_name)
                if btn:
                    btn.clicked.connect(lambda _, i=idx: self.sw.setCurrentIndex(i))

        # conectar acciones comunes
        regresar = getattr(self, "boton_regresar", None) or self.findChild(QPushButton, "boton_regresar")
        if regresar:
            regresar.clicked.connect(self.on_regresar)

        # conectar posible botón de cerrar sesión -> volver al login
        for name in ("boton_cerrar_sesion", "boton_cerrar", "pushButton_cerrar", "btn_cerrar_sesion", "cerrarSesion"):
            b = getattr(self, name, None) or self.findChild(QPushButton, name)
            if b:
                b.clicked.connect(self.logout_to_login)
                break

        # copiar stylesheet desde la fuente si existe
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

    def on_regresar(self):
        app = QApplication.instance()
        try:
            self.close()
            sel = getattr(app, "selection_window", None)
            if sel:
                sel.show()
                sel.raise_()
                try:
                    sel.activateWindow()
                except Exception:
                    pass
        except Exception:
            traceback.print_exc()

    def logout_to_login(self):
        app = QApplication.instance()
        try:
            # cerrar catálogos si existen
            cw = getattr(app, "client_window", None)
            if cw:
                try: cw.close()
                except Exception: pass
                try: delattr(app, "client_window")
                except Exception: pass
            pw = getattr(app, "product_window", None)
            if pw:
                try: pw.close()
                except Exception: pass
                try: delattr(app, "product_window")
                except Exception: pass
            sel = getattr(app, "selection_window", None)
            if sel:
                try: sel.close()
                except Exception: pass
                try: delattr(app, "selection_window")
                except Exception: pass
            main = getattr(app, "main_window", None)
            if main:
                try:
                    try:
                        if hasattr(main, "stackedWidget"):
                            main.stackedWidget.setCurrentIndex(0)
                    except Exception:
                        pass
                    main.show()
                    main.raise_()
                    try: main.activateWindow()
                    except Exception: pass
                except Exception:
                    traceback.print_exc()
        except Exception:
            traceback.print_exc()

class ProductWindow(QMainWindow):
    def __init__(self, style_source=None):
        super().__init__()
        safe_load_ui(UI_PRODUCTOS, self)
        self.setWindowTitle("Catálogo de Productos")

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
                if getattr(w, "objectName", lambda: None)() == name:
                    return i
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

        regresar = getattr(self, "boton_regresar", None) or self.findChild(QPushButton, "boton_regresar")
        if regresar:
            regresar.clicked.connect(self.on_regresar)

        for name in ("boton_cerrar_sesion", "boton_cerrar", "pushButton_cerrar", "btn_cerrar_sesion", "cerrarSesion"):
            b = getattr(self, name, None) or self.findChild(QPushButton, name)
            if b:
                b.clicked.connect(self.logout_to_login)
                break

        try:
            app = QApplication.instance()
            if app and app.styleSheet():
                self.setStyleSheet(app.styleSheet())
        except Exception:
            pass

    def on_regresar(self):
        app = QApplication.instance()
        try:
            self.close()
            sel = getattr(app, "selection_window", None)
            if sel:
                sel.show()
                sel.raise_()
                try: sel.activateWindow()
                except Exception: pass
        except Exception:
            traceback.print_exc()

    def logout_to_login(self):
        app = QApplication.instance()
        try:
            cw = getattr(app, "client_window", None)
            if cw:
                try: cw.close()
                except Exception: pass
                try: delattr(app, "client_window")
                except Exception: pass
            pw = getattr(app, "product_window", None)
            if pw:
                try: pw.close()
                except Exception: pass
                try: delattr(app, "product_window")
                except Exception: pass
            sel = getattr(app, "selection_window", None)
            if sel:
                try: sel.close()
                except Exception: pass
                try: delattr(app, "selection_window")
                except Exception: pass
            main = getattr(app, "main_window", None)
            if main:
                try:
                    try:
                        if hasattr(main, "stackedWidget"):
                            main.stackedWidget.setCurrentIndex(0)
                    except Exception:
                        pass
                    main.show()
                    main.raise_()
                    try: main.activateWindow()
                    except Exception: pass
                except Exception:
                    traceback.print_exc()
        except Exception:
            traceback.print_exc()

class SelectionWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        safe_load_ui(UI_LOGIN, self)
        self.setWindowTitle("Seleccionar catálogo")
        try:
            if hasattr(self, "stackedWidget"):
                self.stackedWidget.setCurrentIndex(1)
        except Exception:
            pass

        btn_clients = getattr(self, "pushButton_3", None) or self.findChild(QPushButton, "pushButton_3")
        if btn_clients:
            btn_clients.clicked.connect(self.open_clients_catalog)
        btn_products = getattr(self, "pushButton_4", None) or self.findChild(QPushButton, "pushButton_4")
        if btn_products:
            btn_products.clicked.connect(self.open_products_catalog)

        for name in ("boton_cerrar_sesion", "boton_cerrar", "pushButton_cerrar", "btn_cerrar_sesion", "cerrarSesion"):
            b = getattr(self, name, None) or self.findChild(QPushButton, name)
            if b:
                b.clicked.connect(self.logout_to_login)
                break

    def open_clients_catalog(self):
        if not os.path.exists(UI_CLIENTES):
            QMessageBox.critical(self, "Error", f"No se encontró {UI_CLIENTES}")
            return
        try:
            cw = ClientWindow(style_source=self)
        except Exception:
            QMessageBox.critical(self, "Error", "No se pudo abrir el catálogo de clientes.")
            return
        app = QApplication.instance()
        setattr(app, "client_window", cw)
        setattr(app, "selection_window", self)
        cw.show()
        self.hide()

    def open_products_catalog(self):
        if not os.path.exists(UI_PRODUCTOS):
            QMessageBox.critical(self, "Error", f"No se encontró {UI_PRODUCTOS}")
            return
        try:
            pw = ProductWindow(style_source=self)
        except Exception:
            QMessageBox.critical(self, "Error", "No se pudo abrir el catálogo de productos.")
            return
        app = QApplication.instance()
        setattr(app, "product_window", pw)
        setattr(app, "selection_window", self)
        pw.show()
        self.hide()

    def logout_to_login(self):
        app = QApplication.instance()
        try:
            cw = getattr(app, "client_window", None)
            if cw:
                try: cw.close()
                except Exception: pass
                try: delattr(app, "client_window")
                except Exception: pass
            pw = getattr(app, "product_window", None)
            if pw:
                try: pw.close()
                except Exception: pass
                try: delattr(app, "product_window")
                except Exception: pass
            try:
                self.close()
            except Exception:
                pass
            try:
                delattr(app, "selection_window")
            except Exception:
                pass
            main = getattr(app, "main_window", None)
            if main:
                try:
                    try:
                        if hasattr(main, "stackedWidget"):
                            main.stackedWidget.setCurrentIndex(0)
                    except Exception:
                        pass
                    main.show()
                    main.raise_()
                    try: main.activateWindow()
                    except Exception: pass
                except Exception:
                    traceback.print_exc()
        except Exception:
            traceback.print_exc()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        safe_load_ui(UI_LOGIN, self)
        self.setWindowTitle("Iniciar sesión")
        try:
            if hasattr(self, "stackedWidget"):
                self.stackedWidget.setCurrentIndex(0)
        except Exception:
            pass

        btn_login = getattr(self, "pushButton", None) or self.findChild(QPushButton, "pushButton")
        if btn_login:
            btn_login.clicked.connect(self.on_login)
        btn_exit = getattr(self, "pushButton_2", None) or self.findChild(QPushButton, "pushButton_2")
        if btn_exit:
            btn_exit.clicked.connect(QApplication.instance().quit)

    def on_login(self):
        usuario = getattr(self, "lineEdit", None)
        clave = getattr(self, "lineEdit_2", None)
        user_text = usuario.text() if usuario else ""
        pass_text = clave.text() if clave else ""
        if not user_text or not pass_text:
            QMessageBox.warning(self, "Error", "Ingrese usuario y contraseña")
            return
        sel = SelectionWindow(parent=self)
        app = QApplication.instance()
        setattr(app, "selection_window", sel)
        setattr(app, "main_window", self)
        sel.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    setattr(app, "main_window", window)
    window.show()
    sys.exit(app.exec_())
# filepath: /Users/javierramirez/Documents/crupython/main.py
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QStackedWidget
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

        self.sw = getattr(self, "stackedWidget_2", None) or self.findChild(QStackedWidget)

        page_map = {
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
                if getattr(w, "objectName", lambda: None)() == name:
                    return i
            if fallback is not None and 0 <= fallback < self.sw.count():
                return fallback
            return None

        fallback_indices = {
            "page_crear": 0,
            "page_buscar": 1,
            "page_editar": 2,
            "page_listar": 4,
            "page_eliminar": 5,
        }

        if self.sw:
            for btn_name, page_name in page_map.items():
                idx = index_of_page(page_name, fallback_indices.get(page_name))
                if idx is None:
                    continue
                btn = getattr(self, btn_name, None) or self.findChild(QPushButton, btn_name)
                if btn:
                    btn.clicked.connect(lambda _, i=idx: self.sw.setCurrentIndex(i))

        # conectar acciones comunes
        regresar = getattr(self, "boton_regresar", None) or self.findChild(QPushButton, "boton_regresar")
        if regresar:
            regresar.clicked.connect(self.on_regresar)

        # conectar posible botón de cerrar sesión -> volver al login
        for name in ("boton_cerrar_sesion", "boton_cerrar", "pushButton_cerrar", "btn_cerrar_sesion", "cerrarSesion"):
            b = getattr(self, name, None) or self.findChild(QPushButton, name)
            if b:
                b.clicked.connect(self.logout_to_login)
                break

        # copiar stylesheet desde la fuente si existe
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

    def on_regresar(self):
        app = QApplication.instance()
        try:
            self.close()
            sel = getattr(app, "selection_window", None)
            if sel:
                sel.show()
                sel.raise_()
                try:
                    sel.activateWindow()
                except Exception:
                    pass
        except Exception:
            traceback.print_exc()

    def logout_to_login(self):
        app = QApplication.instance()
        try:
            # cerrar catálogos si existen
            cw = getattr(app, "client_window", None)
            if cw:
                try: cw.close()
                except Exception: pass
                try: delattr(app, "client_window")
                except Exception: pass
            pw = getattr(app, "product_window", None)
            if pw:
                try: pw.close()
                except Exception: pass
                try: delattr(app, "product_window")
                except Exception: pass
            sel = getattr(app, "selection_window", None)
            if sel:
                try: sel.close()
                except Exception: pass
                try: delattr(app, "selection_window")
                except Exception: pass
            main = getattr(app, "main_window", None)
            if main:
                try:
                    try:
                        if hasattr(main, "stackedWidget"):
                            main.stackedWidget.setCurrentIndex(0)
                    except Exception:
                        pass
                    main.show()
                    main.raise_()
                    try: main.activateWindow()
                    except Exception: pass
                except Exception:
                    traceback.print_exc()
        except Exception:
            traceback.print_exc()

class ProductWindow(QMainWindow):
    def __init__(self, style_source=None):
        super().__init__()
        safe_load_ui(UI_PRODUCTOS, self)
        self.setWindowTitle("Catálogo de Productos")

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
                if getattr(w, "objectName", lambda: None)() == name:
                    return i
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

        regresar = getattr(self, "boton_regresar", None) or self.findChild(QPushButton, "boton_regresar")
        if regresar:
            regresar.clicked.connect(self.on_regresar)

        for name in ("boton_cerrar_sesion", "boton_cerrar", "pushButton_cerrar", "btn_cerrar_sesion", "cerrarSesion"):
            b = getattr(self, name, None) or self.findChild(QPushButton, name)
            if b:
                b.clicked.connect(self.logout_to_login)
                break

        try:
            app = QApplication.instance()
            if app and app.styleSheet():
                self.setStyleSheet(app.styleSheet())
        except Exception:
            pass

    def on_regresar(self):
        app = QApplication.instance()
        try:
            self.close()
            sel = getattr(app, "selection_window", None)
            if sel:
                sel.show()
                sel.raise_()
                try: sel.activateWindow()
                except Exception: pass
        except Exception:
            traceback.print_exc()

    def logout_to_login(self):
        app = QApplication.instance()
        try:
            cw = getattr(app, "client_window", None)
            if cw:
                try: cw.close()
                except Exception: pass
                try: delattr(app, "client_window")
                except Exception: pass
            pw = getattr(app, "product_window", None)
            if pw:
                try: pw.close()
                except Exception: pass
                try: delattr(app, "product_window")
                except Exception: pass
            sel = getattr(app, "selection_window", None)
            if sel:
                try: sel.close()
                except Exception: pass
                try: delattr(app, "selection_window")
                except Exception: pass
            main = getattr(app, "main_window", None)
            if main:
                try:
                    try:
                        if hasattr(main, "stackedWidget"):
                            main.stackedWidget.setCurrentIndex(0)
                    except Exception:
                        pass
                    main.show()
                    main.raise_()
                    try: main.activateWindow()
                    except Exception: pass
                except Exception:
                    traceback.print_exc()
        except Exception:
            traceback.print_exc()

class SelectionWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        safe_load_ui(UI_LOGIN, self)
        self.setWindowTitle("Seleccionar catálogo")
        try:
            if hasattr(self, "stackedWidget"):
                self.stackedWidget.setCurrentIndex(1)
        except Exception:
            pass

        btn_clients = getattr(self, "pushButton_3", None) or self.findChild(QPushButton, "pushButton_3")
        if btn_clients:
            btn_clients.clicked.connect(self.open_clients_catalog)
        btn_products = getattr(self, "pushButton_4", None) or self.findChild(QPushButton, "pushButton_4")
        if btn_products:
            btn_products.clicked.connect(self.open_products_catalog)

        for name in ("boton_cerrar_sesion", "boton_cerrar", "pushButton_cerrar", "btn_cerrar_sesion", "cerrarSesion"):
            b = getattr(self, name, None) or self.findChild(QPushButton, name)
            if b:
                b.clicked.connect(self.logout_to_login)
                break

    def open_clients_catalog(self):
        if not os.path.exists(UI_CLIENTES):
            QMessageBox.critical(self, "Error", f"No se encontró {UI_CLIENTES}")
            return
        try:
            cw = ClientWindow(style_source=self)
        except Exception:
            QMessageBox.critical(self, "Error", "No se pudo abrir el catálogo de clientes.")
            return
        app = QApplication.instance()
        setattr(app, "client_window", cw)
        setattr(app, "selection_window", self)
        cw.show()
        self.hide()

    def open_products_catalog(self):
        if not os.path.exists(UI_PRODUCTOS):
            QMessageBox.critical(self, "Error", f"No se encontró {UI_PRODUCTOS}")
            return
        try:
            pw = ProductWindow(style_source=self)
        except Exception:
            QMessageBox.critical(self, "Error", "No se pudo abrir el catálogo de productos.")
            return
        app = QApplication.instance()
        setattr(app, "product_window", pw)
        setattr(app, "selection_window", self)
        pw.show()
        self.hide()

    def logout_to_login(self):
        app = QApplication.instance()
        try:
            cw = getattr(app, "client_window", None)
            if cw:
                try: cw.close()
                except Exception: pass
                try: delattr(app, "client_window")
                except Exception: pass
            pw = getattr(app, "product_window", None)
            if pw:
                try: pw.close()
                except Exception: pass
                try: delattr(app, "product_window")
                except Exception: pass
            try:
                self.close()
            except Exception:
                pass
            try:
                delattr(app, "selection_window")
            except Exception:
                pass
            main = getattr(app, "main_window", None)
            if main:
                try:
                    try:
                        if hasattr(main, "stackedWidget"):
                            main.stackedWidget.setCurrentIndex(0)
                    except Exception:
                        pass
                    main.show()
                    main.raise_()
                    try: main.activateWindow()
                    except Exception: pass
                except Exception:
                    traceback.print_exc()
        except Exception:
            traceback.print_exc()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        safe_load_ui(UI_LOGIN, self)
        self.setWindowTitle("Iniciar sesión")
        try:
            if hasattr(self, "stackedWidget"):
                self.stackedWidget.setCurrentIndex(0)
        except Exception:
            pass

        btn_login = getattr(self, "pushButton", None) or self.findChild(QPushButton, "pushButton")
        if btn_login:
            btn_login.clicked.connect(self.on_login)
        btn_exit = getattr(self, "pushButton_2", None) or self.findChild(QPushButton, "pushButton_2")
        if btn_exit:
            btn_exit.clicked.connect(QApplication.instance().quit)

    def on_login(self):
        usuario = getattr(self, "lineEdit", None)
        clave = getattr(self, "lineEdit_2", None)
        user_text = usuario.text() if usuario else ""
        pass_text = clave.text() if clave else ""
        if not user_text or not pass_text:
            QMessageBox.warning(self, "Error", "Ingrese usuario y contraseña")
            return
        sel = SelectionWindow(parent=self)
        app = QApplication.instance()
        setattr(app, "selection_window", sel)
        setattr(app, "main_window", self)
        sel.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    setattr(app, "main_window", window)
    window.show()
    sys.exit(app.exec_())