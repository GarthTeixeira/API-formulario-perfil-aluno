FROM python:3.12.6

WORKDIR /app
# Copy the requirements file from the parent directory
COPY ../requirements.txt .
# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
# Copy the rest of the application from the parent directory
COPY ../ .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run"]