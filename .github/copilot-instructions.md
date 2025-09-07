# Copilot Instructions for zerocode-tgbot-builder

## Project Overview
- **Purpose:** Instantly generate Telegram bots from draw.io workflows (XML). Users upload XML, pay via TON, and receive a Go bot ready for deployment.
- **Architecture:**
  - **Python bot**: Handles Telegram interaction, XML upload, payment via TON, and delivers the Go bot zip. Stateless except for payment tracking.
  - **Go bot generator (`gobotgen/`)**: Contains Go code templates and logic for the generated bots. User state is managed in Go, not Python.
  - **Workflow:** User sends XML → Python bot parses and validates → User pays TON → Python bot delivers Go bot zip.

## Key Files & Directories
- `main.py`, `bot.py`: Telegram bot logic, user flow, file handling, payment.
- `db.py`: Async SQLite for payment/user state (Python side only).
- `payment.py`, `WalletManager.py`: TON payment logic, unique comment per user.
- `models.py`, `xml2graph.py`: XML-to-graph conversion, immutable Node/Edge, step-by-step debug prints.
- `gobotgen/`: Go bot generator, stateful user logic, Dockerfile, config.yaml.
- `secrets.yaml`: All secrets/config (excluded from git).
- `docker-compose.yml`, `Dockerfile`: Dockerized for both Python and Go bots.

## Developer Workflows
- **Run Python bot:** `python main.py` (or use Docker Compose)
- **Build/Run Go bot:** See `gobotgen/Dockerfile` and `gobotgen/main.go`. Use Go 1.22+.
- **Testing XML-to-graph:** Run `python xml2graph.py` for debug output.
- **Secrets:** Place all secrets in `secrets.yaml` (never commit to git).
- **Add new Go bot logic:** Edit `gobotgen/` files. User state is managed in Go (`state.go`).

## Patterns & Conventions
- **Python:**
  - All stateful logic (except payment) is in Go bots, not Python.
  - Use immutable, hashable dataclasses for graph nodes/edges.
  - Payment status tracked in SQLite (`user_states.db`).
  - All config/secrets loaded from `secrets.yaml` via `config.py`.
- **Go:**
  - User state is tracked in SQLite (`state.go`).
  - Bot logic is generated based on parsed XML.
- **Docker:**
  - Both Python and Go bots are containerized. Use `docker-compose.yml` for orchestration.
- **Security:**
  - Never commit `secrets.yaml` or any secrets to git.

## Integration Points
- **TON Payment:** Real TON payment via WalletManager, unique comment per user for tracking.
- **XML Workflow:** draw.io XML is parsed to a graph, which is used to generate Go bot logic.
- **Bot Delivery:** After payment, user receives a Go bot zip archive.

## Examples
- See `xml2graph.py` for step-by-step debug output of XML parsing.
- See `gobotgen/main.go` and `gobotgen/state.go` for Go bot state logic.
- See `README.md` for workflow diagrams and usage scenarios.

---

For any unclear or incomplete sections, please provide feedback to improve these instructions.
