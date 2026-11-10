# Berkontribusi

Pasang dependensi:

```
pip install -r requirements-lock.txt
pip install -e ".[dev]"
```

Cek sebelum commit:

```
ruff check .
mypy builderguild/builderguild commander.py
pytest --cov=builderguild --cov=commander --cov-fail-under=70
```

Satu perubahan per commit, bersama tesnya.
