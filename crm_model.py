import sqlite3
from datetime import datetime

class CRMModel:
    def __init__(self, db_path='clientes.db'):
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

    def obtener_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def obtener_cliente(self, cliente_id):
        self.cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        return self.cursor.fetchone()

    def agregar_cliente(self, nombre, telefono, ultima_compra, frecuencia):
        self.cursor.execute("""
            INSERT INTO clientes (nombre, telefono, ultima_compra, frecuencia)
            VALUES (?, ?, ?, ?)""", (nombre, telefono, ultima_compra, frecuencia))
        self.conn.commit()
        return self.cursor.lastrowid

    def actualizar_cliente(self, cliente_id, nombre, telefono, ultima_compra, frecuencia):
        self.cursor.execute("""
            UPDATE clientes
            SET nombre = ?, telefono = ?, ultima_compra = ?, frecuencia = ?
            WHERE id = ?
        """, (nombre, telefono, ultima_compra, frecuencia, cliente_id))
        self.conn.commit()
        return self.cursor.rowcount

    def eliminar_cliente(self, cliente_id):
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        self.conn.commit()
        return self.cursor.rowcount
