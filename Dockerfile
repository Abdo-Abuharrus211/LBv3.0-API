LABEL authors="ABDULQADIR ABUHARRUS"

FROM python:3.13
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
#RUN useradd --create-home appuser
#USER appuser
EXPOSE 8000
CMD ["gunincorn", "-w", "4", "-b", "0000:8000", "app:app"]