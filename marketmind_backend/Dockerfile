# FROM python:3.9-slim

# ARG SERVICE_NAME

# WORKDIR /app

# # Copy the specific service code
# COPY ${SERVICE_NAME}/ /app/

# # Copy common requirements
# COPY ${SERVICE_NAME}/requirements.txt /app/requirements.txt

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the Flask port
# EXPOSE 5000

# # Start the service
# CMD ["python", "app.py"]

FROM python:3.9-slim
ARG SERVICE_NAME
WORKDIR /app
COPY ${SERVICE_NAME}/ /app/
COPY ${SERVICE_NAME}/requirements.txt /app/requirements.txt

# Debug step: Print requirements.txt
RUN cat /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Debug step: Confirm installed versions
RUN pip freeze | grep -E "Flask|Werkzeug"

EXPOSE 5000
CMD ["python", "app.py"]