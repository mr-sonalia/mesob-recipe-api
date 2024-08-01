ARG PYTHON_VERSION=3.10.11
ARG USER=appuser
ARG APPLICATION_PORT=8000

FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
	--disabled-password \
	--gecos "" \
	--home "/nonexistent" \
	--shell "/sbin/nologin" \
	--no-create-home \
	--uid "${UID}" \
	appuser

# Install the OS dependencies.
RUN apt update \
	&& apt install libpq-dev gcc -y \
	&& pip install psycopg2


# Download dependencies as a separate step to take advantage of Docker's caching.
RUN python -m pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache/pip \
	--mount=type=bind,source=requirements.txt,target=requirements.txt \
	python -m pip install -r requirements.txt


# Copy the source code into the container.
COPY . .

# Expose the port that the application runs on.
EXPOSE ${APPLICATION_PORT}

#  Run celery worker
# COPY ./start-scripts/django.bash /app/start-server
# RUN sed -i 's/\r$//g' /start-celeryworker
# RUN chmod +x /app/start-server

#  Run celery worker
# COPY ./start-scripts/worker.bash /app/start-celeryworker
# RUN sed -i 's/\r$//g' /start-celeryworker
# RUN chmod +x /app/start-celeryworker

# Run celery beat
# COPY ./start-scripts/beat.bash /app/start-celerybeat
# RUN sed -i 's/\r$//g' /start-celerybeat
# RUN chmod +x /app/start-celerybeat

# Switch to the non-privileged user to run the application.
USER appuser

#  Run migrations
# RUN python manage.py migrate

# Run the application.
CMD  gunicorn config.wsgi:application --bind 0.0.0.0:8000