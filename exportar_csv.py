import sqlite3
import pandas as pd

def exportar_clientes_a_csv():
    conn = sqlite3.connect("clientes.db")
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    df.to_csv("clientes_exportados.csv", index=False)
    print("✅ Archivo CSV exportado como 'clientes_exportados.csv'")

if __name__ == "__main__":
    exportar_clientes_a_csv()
