# Python Topics to Master — AI Security Fellows Prep (with Official Docs)

> Each topic links to its official documentation: `docs.python.org` for standard-library topics, and the library's own official docs site for third-party topics (no blogs/tutorials/Stack Overflow).

## 1. Core Language & Idioms
- [Type hints & static typing (`typing`)](https://docs.python.org/3/library/typing.html)
- [Dataclasses (`@dataclass`)](https://docs.python.org/3/library/dataclasses.html)
- [Pydantic models](https://docs.pydantic.dev/latest/)
- [Context managers (`contextlib`)](https://docs.python.org/3/library/contextlib.html)
- [Decorators (function definitions reference)](https://docs.python.org/3/glossary.html#term-decorator)
- [Generators & iterators](https://docs.python.org/3/tutorial/classes.html#generators)
- [`struct` — binary data packing/unpacking](https://docs.python.org/3/library/struct.html)
- [`bytes`/`bytearray` & bitwise operations](https://docs.python.org/3/library/stdtypes.html#bytes-objects)
- [Exception handling](https://docs.python.org/3/tutorial/errors.html)
- [`enum`](https://docs.python.org/3/library/enum.html)
- [`re` — regular expressions](https://docs.python.org/3/library/re.html)

## 2. Concurrency & Async
- [`asyncio`](https://docs.python.org/3/library/asyncio.html)
- [`threading`](https://docs.python.org/3/library/threading.html)
- [`queue`](https://docs.python.org/3/library/queue.html)
- [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
- [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html)
- [`subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Lock objects / race-condition prevention](https://docs.python.org/3/library/threading.html#lock-objects)

## 3. Networking & Protocols
- [`socket`](https://docs.python.org/3/library/socket.html)
- [pySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [HTTPX](https://www.python-httpx.org/)
- [`http.server`](https://docs.python.org/3/library/http.server.html)
- [websockets](https://websockets.readthedocs.io/en/stable/)
- [dnspython](https://dnspython.readthedocs.io/en/stable/)
- [Scapy](https://scapy.readthedocs.io/en/latest/)
- [pyshark (official repo)](https://github.com/KimiNewt/pyshark)

## 4. Web Frameworks & API Design
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [REST API design — FastAPI "First Steps"](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
- [Flask-Limiter (rate limiting)](https://flask-limiter.readthedocs.io/en/stable/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)

## 5. Data & Persistence
- [`sqlite3`](https://docs.python.org/3/library/sqlite3.html)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
- [SQLAlchemy (ORM)](https://docs.sqlalchemy.org/en/20/)
- [`json`](https://docs.python.org/3/library/json.html)
- [`csv`](https://docs.python.org/3/library/csv.html)

## 6. Security-Specific Libraries
- [`cryptography`](https://cryptography.io/en/latest/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [Open Policy Agent (OPA) / Rego](https://www.openpolicyagent.org/docs/latest/)
- [SPIFFE/SPIRE](https://spiffe.io/docs/latest/spire-about/)
- [liboqs-python (post-quantum crypto bindings)](https://github.com/open-quantum-safe/liboqs-python)

## 7. Testing & Quality
- [pytest](https://docs.pytest.org/en/stable/)
- [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html)
- [responses (HTTP mocking)](https://github.com/getsentry/responses)
- [coverage.py](https://coverage.readthedocs.io/en/latest/)

## 8. CLI & Tooling
- [`argparse`](https://docs.python.org/3/library/argparse.html)
- [Click](https://click.palletsprojects.com/en/stable/)
- [`curses`](https://docs.python.org/3/library/curses.html)
- [Python Packaging User Guide (pyproject.toml)](https://packaging.python.org/en/latest/)
- [`logging`](https://docs.python.org/3/library/logging.html)

## 9. Data Science / ML for Security
- [NumPy](https://numpy.org/doc/stable/)
- [pandas](https://pandas.pydata.org/docs/)
- [scikit-learn](https://scikit-learn.org/stable/)
- [XGBoost](https://xgboost.readthedocs.io/en/stable/)
- [PyTorch](https://pytorch.org/docs/stable/index.html)
- [joblib](https://joblib.readthedocs.io/en/stable/)
- [`hashlib` (SHA-256)](https://docs.python.org/3/library/hashlib.html)

## 10. Signal Processing / SDR
- [GNU Radio Guided Tutorials (incl. embedded Python blocks)](https://tutorials.gnuradio.org)
- NumPy correlation/DSP — see NumPy link above

## 11. Software Design Patterns
- [Flask application factory pattern](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)
- [FastAPI dependency injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Python data model reference (general OOP mechanics)](https://docs.python.org/3/reference/datamodel.html)
- *Repository pattern / MVC / state machines — general software-engineering concepts with no single canonical official doc; best learned via the framework docs above applied in practice.*

## 12. Distributed/Systems Concepts
- [Apache Kafka documentation](https://kafka.apache.org/documentation/)
- [kafka-python (client library)](https://kafka-python.readthedocs.io/en/master/)
- [`signal` (SIGTERM/SIGKILL handling)](https://docs.python.org/3/library/signal.html)
- *Health checks / readiness probes — general pattern, no single canonical official doc.*
