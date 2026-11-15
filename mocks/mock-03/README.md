# Wallet core (Mock 2)

The wallet core for a small payments app. A `Wallet` holds balances in USD, USDC and EUR
and keeps a transaction history. Money is moved between wallets with a fee, and can be
converted between currencies inside one wallet.

## Layout

```
wallet/
  errors.py     exceptions
  money.py      turning caller input into safe Decimal amounts; supported currencies
  wallet.py     Wallet: balance, deposit, withdraw, history
  transfers.py  transfer between wallets with a 0.5% fee (min 0.01) paid by the sender
  fx.py         currency conversion inside a wallet
tests/          pytest suite
```

## Running

```
pip install pytest
python -m pytest -v
```

Some tests currently fail. Your interviewer will walk you through the task.
