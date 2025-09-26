FROM python:3.12

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /src

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /src
COPY --chown=user . /src

CMD ["uvicorn", "app:server", "--host", "0.0.0.0", "--port", "7860"]