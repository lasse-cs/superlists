FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /src
# Install dependencies
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN uv sync --locked --no-install-project

ENV PATH="/src/.venv/bin:$PATH"

COPY src /src

RUN python manage.py collectstatic

ENV DJANGO_DEBUG_FALSE=1
RUN adduser --uid 1234 nonroot
USER nonroot

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]
