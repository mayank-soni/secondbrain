# 
FROM python:3.9

# 
WORKDIR /backend/

# 
COPY ./requirements.txt /backend/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# 
COPY ./backend /backend

COPY ./data /data
# Load the secret into an environment variable
# RUN echo "export OPENAI_API_KEY=$(cat ./api_key.txt)" > /backend/src/fastapi/load_api_key.sh
# RUN echo "export OPENAI_API_KEY=$(cat run/build/secrets/api_key)" > /backend/src/fastapi/load_api_key.sh
# Make the script executable
# RUN chmod +x /backend/src/fastapi/load_api_key.sh
#ENV OPENAI_API_KEY=""
# 
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# ENTRYPOINT ["/bin/bash", "-c", "cat run/build/secrets/api_key && source load_api_key.sh && uvicorn backend:app --host 0.0.0.0 --port 80"]
# ENTRYPOINT ["/bin/bash", "-c", "echo \"$OPENAI_API_KEY\" && source load_api_key.sh && uvicorn backend:app --host 0.0.0.0 --port 80"]
ENTRYPOINT ["/bin/bash", "-c", "echo \"$OPENAI_API_KEY\" && uvicorn src.fastapi.backend_utils:app --host 0.0.0.0 --port 80"]