FROM python:3.13-slim
LABEL authors="ABDULQADIR ABUHARRUS"
WORKDIR /usr/src/app
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#RUN useradd --create-home appuser
#USER appuser
EXPOSE 8000
CMD ["gunincorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]