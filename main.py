from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import uvicorn

app = FastAPI()

# Configuración de la conexión a la base de datos
# Se utiliza el formato correcto para la URL de conexión
database_url = "postgresql://databasemenu_user:ZnoY5wh7SjJ3aybp42olfAeaR6xmzWWm@dpg-ckr9rehrfc9c73djbtu0-a/databasemenu"

# Modelo de datos para el pedido
class Pedido(BaseModel):
    cliente: str
    total: float
    estado_pedido: str
    fecha_pedido: str

# Ruta para obtener todos los pedidos
@app.get('/pedidos')
def get_pedidos():
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedido")
    pedidos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    return pedidos

# Ruta para crear un nuevo pedido
@app.post('/pedidos')
def create_pedido(pedido: Pedido):
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    cliente = pedido.cliente
    total = pedido.total
    estado_pedido = pedido.estado_pedido
    fecha_pedido = pedido.fecha_pedido

    cursor.execute("INSERT INTO pedido (cliente, total, estado_pedido, fecha_pedido) VALUES (%s, %s, %s, %s)",
                   (cliente, total, estado_pedido, fecha_pedido))
    conn.commit()

    # Obtén el ID del pedido recién creado
    cursor.execute("SELECT lastval()")
    pedido_id = cursor.fetchone()[0]
    conn.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    return {'mensaje': 'Pedido creado', 'pedido_id': pedido_id}

# Ruta para obtener un pedido por ID
@app.get('/pedidos/{pedido_id}')
def get_pedido(pedido_id: int):
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedido WHERE id = %s", (pedido_id,))
    pedido = cursor.fetchone()
    if pedido:
        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()
        return pedido
    raise HTTPException(status_code=404, detail='Pedido no encontrado')

# Ruta para actualizar un pedido por ID
@app.put('/pedidos/{pedido_id}')
def update_pedido(pedido_id: int, pedido: Pedido):
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    cliente = pedido.cliente
    total = pedido.total
    estado_pedido = pedido.estado_pedido
    fecha_pedido = pedido.fecha_pedido

    cursor.execute("UPDATE pedido SET cliente = %s, total = %s, estado_pedido = %s, fecha_pedido = %s WHERE id = %s",
                   (cliente, total, estado_pedido, fecha_pedido, pedido_id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    return {'mensaje': 'Pedido actualizado'}

# Ruta para eliminar un pedido por ID
@app.delete('/pedidos/{pedido_id}')
def delete_pedido(pedido_id: int):
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
    conn.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    return {'mensaje': 'Pedido eliminado'}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

