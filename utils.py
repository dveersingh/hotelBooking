from passlib.hash import bcrypt
from datetime import datetime, timedelta
from jose import jwt

SECRET = "ultrasecurekey123"
JWT_ALGO = "HS256"

def hash_password(password):
    return bcrypt.hash(password)

def check_password(plain_text, hashed_text):
    return bcrypt.verify(plain_text, hashed_text)

def generate_jwt(data: dict, expiry: timedelta):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + expiry})
    return jwt.encode(payload, SECRET, algorithm=JWT_ALGO)

class SegmentTree:
    def __init__(self, rates):
        self.n = len(rates)
        self.tree = [0] * (4 * self.n)
        self.build(0, 0, self.n - 1, rates)

    def build(self, node, start, end, rates):
        if start == end:
            self.tree[node] = rates[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node + 1, start, mid, rates)
            self.build(2 * node + 2, mid + 1, end, rates)
            self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])

    def query(self, node, start, end, left, right):
        if start > right or end < left:
            return float('inf')
        if start >= left and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        left_query = self.query(2 * node + 1, start, mid, left, right)
        right_query = self.query(2 * node + 2, mid + 1, end, left, right)
        return min(left_query, right_query)
