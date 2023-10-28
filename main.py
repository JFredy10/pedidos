from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos para el pedido
class Pedido(BaseModel):
    id: int
    cliente: str
    total: float
    estado_pedido: str
    fecha_pedido: str

# Lista en memoria para almacenar los pedidos
pedidos = []

# Ruta para obtener todos los pedidos
@app.get('/pedidos')
def get_pedidos():
    return pedidos

# Ruta para crear un nuevo pedido
@app.post('/pedidos')
def create_pedido(pedido: Pedido):
    pedidos.append(pedido)
    return {'mensaje': 'Pedido creado'}

# Ruta para obtener un pedido por ID
@app.get('/pedidos/{pedido_id}')
def get_pedido(pedido_id: int):
    for pedido in pedidos:
        if pedido.id == pedido_id:
            return pedido
    raise HTTPException(status_code=404, detail='Pedido no encontrado')

# Ruta para actualizar un pedido por ID
@app.put('/pedidos/{pedido_id}')
def update_pedido(pedido_id: int, pedido: Pedido):
    for i, p in enumerate(pedidos):
        if p.id == pedido_id:
            pedidos[i] = pedido
            return {'mensaje': 'Pedido actualizado'}
    raise HTTPException(status_code=404, detail='Pedido no encontrado')

# Ruta para eliminar un pedido por ID
@app.delete('/pedidos/{pedido_id}')
def delete_pedido(pedido_id: int):
    for i, pedido in enumerate(pedidos):
        if pedido.id == pedido_id:
            del pedidos[i]
            return {'mensaje': 'Pedido eliminado'}
    raise HTTPException(status_code=404, detail='Pedido no encontrado')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
