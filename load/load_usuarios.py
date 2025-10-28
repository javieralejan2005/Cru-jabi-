import traceback
from modelo.conexionbd import ConexionBd

try:
    import bcrypt
except Exception:
    bcrypt = None

def authenticate(username: str, password: str):
    """
    Retorna (ok: bool, user: dict|None).
    Asume tabla 'usuarios' con columnas 'usuario' y 'contraseña'.
    Usa bcrypt si el hash está presente y el paquete está instalado.
    """
    if not username or not password:
        return False, None

    db = ConexionBd()
    db.establecerConexionBD()
    if not getattr(db, "conexion", None):
        return False, None

    try:
        cur = db.conexion.cursor()

        # aliasar 'contraseña' a 'pwd' para evitar problemas con caracteres especiales
        # usar corchetes [] para compatibilidad con SQL Server y SQLite
        sql = "SELECT usuario AS usr, [contraseña] AS pwd FROM usuarios WHERE usuario = ?"
        cur.execute(sql, (username,))
        row = cur.fetchone()
        if not row:
            return False, None

        # obtener valores (soporta tanto pyodbc.Row como tuplas)
        try:
            user_name = getattr(row, "usr")
            pwd = getattr(row, "pwd")
        except Exception:
            user_name = row[0]
            pwd = row[1]

        user = {"usuario": user_name}

        # comprobar bcrypt si corresponde
        try:
            pwd_bytes = pwd if isinstance(pwd, (bytes, bytearray)) else str(pwd).encode("utf-8")
            pwd_str = pwd_bytes.decode("utf-8", errors="ignore")
            if bcrypt and pwd_str.startswith("$2"):
                ok = bcrypt.checkpw(password.encode("utf-8"), pwd_bytes)
                return bool(ok), user if ok else (False, None)[1]
        except Exception:
            pass

        # fallback: comparación en texto plano
        if str(pwd) == password:
            return True, user
        return False, None

    except Exception:
        traceback.print_exc()
        return False, None
    finally:
        try:
            db.cerrarConexionBD()
        except Exception:
            pass