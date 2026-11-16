from __future__ import annotations

from decimal import Decimal, InvalidOperation

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from txns.store import Store, seeded


class TxnIn(BaseModel):
    merchant_id: str
    amount: str
    currency: str = "USD"


def create_app(store: Store | None = None) -> FastAPI:
    app = FastAPI()
    store = store or seeded()
    app.state.store = store

    @app.get("/transactions/{txn_id}")
    def get_txn(txn_id: str):
        t = store.get(txn_id)
        if t is None:
            return JSONResponse({"error": {"code": "not_found", "message": f"no transaction {txn_id}"}}, status_code=404)
        return t.to_json()

    @app.post("/transactions", status_code=201)
    def create_txn(body: TxnIn):
        try:
            amount = Decimal(body.amount)
        except InvalidOperation:
            return JSONResponse({"error": {"code": "invalid_amount", "message": "amount must be a number"}}, status_code=400)
        if amount <= 0:
            return JSONResponse({"error": {"code": "invalid_amount", "message": "amount must be positive"}}, status_code=400)
        if not body.merchant_id:
            return JSONResponse({"error": {"code": "invalid_merchant", "message": "merchant_id is required"}}, status_code=400)
        return store.add(body.merchant_id, amount, body.currency).to_json()

    return app
