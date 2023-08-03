# file: orders/api/api.py

import time
import uuid

from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
)

order = {
    'id': '5493248e-5125-4a06-983d-06c54bac43c4',
    'status': "delivered",
    'created': datetime.utcnow(),
    'updated': datetime.utcnow(),
    'order': [
        {
            'product': 'cappuccino',
            'size': 'medium',
            'quantity': 1
        }
    ]
}

orders = []

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    return {'orders': orders}

@app.post('/orders',
          status_code=status.HTTP_201_CREATED,
          response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    orders.append(order)
    return order

@app.get('/orders/{order_id}',
          response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.put('/orders/{order_id}',
          response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
    raise HTTPException (
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    for index, order in enumberate(orders):
        if order['id'] == order_id:
            orders.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise HTTPException (
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.post('/orders/{order_id}/cancel',
          response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
    raise HTTPException (
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.post('/orders/{order_id}/pay',
          response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException (
        status_code=404, detail=f'Order with ID {order_id} not found'
    )
