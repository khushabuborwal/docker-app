# Use Alpine-based image for a smaller footprint
FROM python:3.9.18-alpine3.18 AS builder

WORKDIR /app

# Install necessary build tools (only in the builder stage)
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --target /app/deps -r requirements.txt && \
    find /app/deps -name '*.so' -exec strip --strip-unneeded {} + && \
    find /app/deps -type d -name '__pycache__' -exec rm -rf {} + && \
    find /app/deps -type d -name '*.dist-info' -exec rm -rf {} +

# Ensure the NLTK data directory exists before downloading
RUN mkdir -p /app/nltk_data && \
    PYTHONPATH="/app/deps" python -c "import nltk; nltk.data.path.append('/app/nltk_data'); nltk.download('punkt', download_dir='/app/nltk_data'); nltk.download('punkt_tab', download_dir='/app/nltk_data')"

# Copy text files into the builder stage (for debugging purposes)
COPY IF-1.txt /home/data/IF-1.txt
COPY AlwaysRememberUsThisWay-1.txt /home/data/AlwaysRememberUsThisWay-1.txt

# Final minimal image without unnecessary build tools
FROM python:3.9.18-alpine3.18

WORKDIR /app

# Copy only necessary dependencies and scripts from builder
COPY --from=builder /app/deps /app/deps
COPY --from=builder /app/nltk_data /app/nltk_data
COPY scripts.py .

# Copy text files into the final image
COPY --from=builder /home/data/IF-1.txt /home/data/IF-1.txt
COPY --from=builder /home/data/AlwaysRememberUsThisWay-1.txt /home/data/AlwaysRememberUsThisWay-1.txt

# Ensure Python finds dependencies
ENV PYTHONPATH="/app/deps"
ENV NLTK_DATA="/app/nltk_data"

# Remove unnecessary cache files
RUN rm -rf /var/cache/apk/* /root/.cache

CMD ["python", "scripts.py"]