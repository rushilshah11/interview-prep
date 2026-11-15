SENT: list[tuple[str, str]] = []


def send_email(to: str, body: str) -> None:
    SENT.append((to, body))
