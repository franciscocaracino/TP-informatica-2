import sqlite3
from cliente import Cliente
from datetime import datetime
import pandas as pd

class CRM:
    def __init__(self, db_path="clientes.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                ultima_compra TEXT NOT NULL,
                frecuencia INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def agregar_cliente(self, nombre, telefono, ultima_compra, frecuencia):
        self.cursor.execute("INSERT INTO clientes (nombre, telefono, ultima_compra, frecuencia) VALUES (?, ?, ?, ?)",
                            (nombre, telefono, ultima_compra, frecuencia))
        self.conn.commit()

    def eliminar_cliente(self, id_):
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", (id_,))
        self.conn.commit()

    def actualizar_ultima_compra(self, id_, nueva_fecha):
        self.cursor.execute("UPDATE clientes SET ultima_compra = ? WHERE id = ?", (nueva_fecha, id_))
        self.conn.commit()

    def obtener_todos(self):
        self.cursor.execute("SELECT * FROM clientes")
        rows = self.cursor.fetchall()
        return [Cliente(*row) for row in rows]

    def exportar_csv(self, archivo="clientes_exportado.csv"):
        self.cursor.execute("SELECT * FROM clientes")
        datos = self.cursor.fetchall()
        columnas = ["id", "nombre", "telefono", "ultima_compra", "frecuencia"]
        df = pd.DataFrame(datos, columns=columnas)
        df.to_csv(archivo, index=False)
