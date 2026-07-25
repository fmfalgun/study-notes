# Python Topics to Master — AI Security Fellows Prep

## 1. Core Language & Idioms
- Type hints & static typing (`typing`, generics, `Protocol`)
- Dataclasses (`@dataclass`) vs Pydantic models
- Context managers (`with`, `@contextmanager`) — esp. DB connection/cursor patterns
- Decorators (auth, RBAC, audit-logging, retry/rate-limit decorators)
- Generators & iterators (streaming packet/log processing)
- `struct` / `bytes` / `bytearray` / bitwise operations (binary protocol parsing, CRC/checksum, LFSR dewhitening)
- Exception handling patterns (fail-closed vs fail-open design)
- `enum` for state machines / protocol states
- Regex (`re`) for log/report parsing

## 2. Concurrency & Async
- `asyncio` (event loops, tasks, `async`/`await`)
- `threading` + `queue.Queue` (producer/consumer, worker pools)
- `multiprocessing` / `concurrent.futures` (thread vs process pools)
- `subprocess` (invoking external tools: `opa`, `nmap`, `whatweb`, etc.)
- Race conditions, locks, thread-safety in shared state (device registries, caches)

## 3. Networking & Protocols
- `socket` programming (raw TCP/UDP, serial-over-socket)
- Serial communication (`pyserial`) — AT-command radios, XBee API frames
- HTTP clients (`requests`, `httpx`) and building HTTP servers (stdlib `http.server`, Flask, FastAPI)
- WebSockets / Server-Sent Events (SSE) for real-time push
- DNS resolution internals (`dnspython` or manual socket-based resolution)
- Packet capture/parsing (`scapy`, `pyshark`, raw PCAP read/write)

## 4. Web Frameworks & API Design
- Flask (blueprints, app factories, request/response lifecycle)
- FastAPI (Pydantic request/response models, dependency injection, routers)
- REST API design (status codes, pagination, versioning)
- Middleware patterns (JWT auth, CORS, rate limiting, RBAC)
- Flask-SocketIO / WebSocket-based notification services

## 5. Data & Persistence
- SQLite (`sqlite3`, WAL mode, schema migration)
- MySQL (`mysql-connector-python`, connection pooling)
- ORM vs raw SQL / repository pattern (EAV data modeling)
- Caching strategies (TTL caching, staleness invalidation)
- JSON/CSV/PCAP serialization and schema evolution

## 6. Security-Specific Libraries
- `cryptography` (AES-GCM, X.509 cert generation/verification, PEM handling)
- JWT (`pyjwt`) — issuance, verification, expiry handling
- `bcrypt` / password hashing
- OPA/Rego integration patterns (REST client, CLI subprocess evaluation)
- SPIFFE/SPIRE workload identity concepts in Python
- Post-quantum crypto primitives (ML-KEM, ML-DSA) — library bindings (`liboqs-python` or similar)

## 7. Testing & Quality
- `pytest` (fixtures, parametrize, mocking with `unittest.mock`)
- Test doubles for DB/network calls (mocked cursors, `responses`/`httpx` mocking)
- Integration vs unit test structuring
- `coverage.py`

## 8. CLI & Tooling
- `argparse` / `click` for CLI design
- `curses` for TUI dashboards
- Packaging (`setup.py`/`pyproject.toml`, entry points, `python -m` execution)
- Logging (`logging` module — handlers, rotating file logs, structured logs)

## 9. Data Science / ML for Security
- `numpy` / `pandas` (feature engineering, vectorized signal correlation)
- `scikit-learn` (Random Forest, Isolation Forest, train/test split, confusion matrix)
- `xgboost`
- `PyTorch` (autoencoders, tensors, training loops)
- Model persistence & integrity (`joblib`, SHA-256 checksum manifests)
- Class imbalance / anomaly-detection evaluation metrics

## 10. Signal Processing / SDR (specialized but relevant)
- GNU Radio embedded Python blocks (`gr.sync_block`, work functions, message ports)
- Digital signal processing basics (correlation, despreading, clock recovery) in NumPy
- Frequency-hopping / channel-hopping control logic

## 11. Software Design Patterns
- Repository pattern (data-access abstraction)
- MVC architecture (controllers/models/views in Flask)
- Factory pattern (app factories, config-driven object creation)
- State machine implementation (device lifecycle: register → authenticate → authorize)
- Dependency injection (FastAPI style)

## 12. Distributed/Systems Concepts (Python implementation angle)
- Message queues / event-driven architectures (Kafka producer/consumer basics)
- Idempotency & retry logic
- Graceful shutdown (`SIGTERM`/`SIGKILL` handling)
- Health checks & readiness probes
