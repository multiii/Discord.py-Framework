import os

from faunadb import query as q
from faunadb.client import FaunaClient

client = FaunaClient(
  domain="db.eu.fauna.com",
  port=443,
  scheme="https",
  secret=os.getenv("FAUNA_KEY"),
)

def get(*args, **kwargs):
  if kwargs.get("ref") is not None:
    result = client.query(
      q.get(kwargs['ref'])
    )

    return result

  exists = client.query(q.exists(
    q.match(
      q.index(kwargs["index"]),
      *kwargs.get("index_args")
    )
  ))

  if exists:
    result = client.query(q.get(
      q.match(
        q.index(kwargs["index"]),
        *kwargs.get("index_args")
      )
    ))

    return result

def get_all(*args, **kwargs):
  exists = client.query(q.exists(
    q.match(
      q.index(kwargs["index"]),
      *kwargs.get("index_args")
    )
  ))

  if exists:
    result = client.query(
      q.paginate(q.match(
        q.index(kwargs["index"]),
        *kwargs.get("index_args")
      ))
    )

    return result

def insert(*args, **kwargs):
  client.query(
    q.create(
      q.collection(kwargs["collection"]),
      {
        "data": kwargs["data"]
      }
    )
  )

def upsert(*args, **kwargs):
  d = get(
    index=kwargs["index"],
    index_args=kwargs.get("index_args")
  )

  if d is not None:
    return client.query(q.update(
      d['ref'],
      {
        "data": kwargs["data"]
      }
    ))

  insert(
    collection=kwargs['collection'],
    data=kwargs['data']
  )

def delete(*args, **kwargs):
  client.query(
    q.delete(kwargs['ref'])
  )