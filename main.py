#!/usr/bin/env python3

from fastapi import FastAPI

import os
import os.path

import yaml
import inspect

DATA_PATH = 'data'

app = FastAPI()


@app.get('/messages')
def get_message(node):
    dir = os.path.join(DATA_PATH, node)
    messages = []

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)

        with open(path, 'r') as file:
            data = file.read()

        message = yaml.safe_load(data)
        messages.append(message)

    return messages


@app.post('/messages')
def post_message(node, id, correlation, causation):
    dir = os.path.join(DATA_PATH, node)
    path = os.path.join(dir, f'{id}.yaml')

    data = inspect.cleandoc(
        f"""
            id: '{id}'
            correlation: '{correlation}'
            causation: '{causation}'
        """
    )

    os.makedirs(dir, exist_ok=True)

    with open(path, 'x') as file:
        file.write(data)


@app.delete('/messages')
def delete_message(node, id):
    dir = os.path.join(DATA_PATH, node)
    path = os.path.join(dir, f'{id}.yaml')

    os.remove(path)

    messages = os.listdir(dir)

    if len(messages) > 0:
        return

    os.rmdir(dir)

    nodes = os.listdir(DATA_PATH)

    if len(nodes) > 0:
        return

    os.rmdir(DATA_PATH)
