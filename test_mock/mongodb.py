import pytest
from pymongo import MongoClient

def mongodb_client():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["hk90"]
    c
    return client