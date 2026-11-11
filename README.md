# HotelAPP Backend

A Django REST Framework backend prototype for hotel housekeeping operations. This repository contains Django models and a housekeeping API view; it is **not** the same repository as the larger [HotelFlow application](https://github.com/JotaC95/HotelApp).

## Who this is for

Developers who want to inspect the housekeeping backend, run it locally and understand which routes are actually connected.

## Current project structure

```text
hotelAPP_backend/   Django settings and root URL configuration
housekeeping/       Models, serializers, views, tests and app URL configuration
manage.py           Django management commands
.env.example        Example configuration values
```

## Quick start

1. Clone the repository and create a virtual environment:

```bash
git clone https://github.com/JotaC95/HotelAPP_back.git
cd HotelAPP_back
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the dependencies used by this Django project. **There is currently no tracked requirements file**, so dependency installation is not reproducible yet. You can provision a temporary local environment with:

```bash
python -m pip install 'Django>=5.2,<5.3' djangorestframework
```

3. Set development-only environment variables. Django reads these from the shell; merely copying `.env.example` does not load them automatically:

```bash
export DJANGO_SECRET_KEY='generate-a-unique-development-secret'
export DJANGO_DEBUG=true
export DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
python manage.py check
python manage.py migrate
python manage.py runserver
```

Use a freshly generated random secret rather than the illustrative placeholder before running Django. On Windows, use the equivalent PowerShell environment variable syntax.

## API and routing status

| URL | Status |
| --- | --- |
| `/admin/` | Registered in the root Django URL configuration |
| `cleaner/my-assignments/` | Declared inside `housekeeping/urls.py`, **but not currently included in the root URL configuration**; not accessible until routing is connected |

The presence of serializers and views does not mean public endpoints are enabled. Inspect `hotelAPP_backend/urls.py` and `housekeeping/urls.py` before attempting requests.

## Security and data handling

- Read [security remediation notes](docs/SECURITY_REMEDIATION.md) before deploying or reusing historical credentials.
- Set `DJANGO_SECRET_KEY` outside version control; keep `DJANGO_DEBUG=false` in production.
- The repository currently tracks `db.sqlite3`. Treat its contents as potentially sensitive; do not use real guest or employee data for demonstrations.
- This is a development prototype, not a production-ready service.

## Troubleshooting

- **`Set DJANGO_SECRET_KEY` error:** export the variable in the same shell used to start Django.
- **Module not found:** ensure the virtual environment is active and install the missing dependency; a pinned requirements file is a pending improvement.
- **404 for assignments:** the housekeeping URL configuration has not been included in the root router.

## Next steps

1. Add a reviewed, pinned requirements file.
2. Connect and document intended housekeeping routes.
3. Add automated API tests and example requests/responses.
4. Remove development database artifacts from future commits after reviewing their contents.
