from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from payouts.ledger import Ledger, PayoutError


def create_app(ledger: Ledger) -> FastAPI:
    app = FastAPI()

    @app.exception_handler(PayoutError)
    def handle_payout_error(request: Request, e: PayoutError):
        return JSONResponse({"error": {"code": e.code, "message": e.message}})

    @app.post("/merchants/{merchant_id}/payouts", status_code=201)
    def create_payout(merchant_id: str):
        return ledger.create_payout(merchant_id)

    @app.get("/merchants/{merchant_id}/payouts")
    def list_payouts(merchant_id: str):
        return {"data": ledger.merchants[merchant_id].payouts}

    return app
