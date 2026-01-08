FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including Node.js and nginx
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    nginx \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY scripts/ ./scripts/
COPY credentials.json ./credentials.json

# Copy frontend code and build
COPY web/ ./web/
WORKDIR /app/web
RUN npm install && npm run build

# Move built frontend to nginx serve directory
RUN mkdir -p /usr/share/nginx/html && \
    cp -r dist/* /usr/share/nginx/html/

# Configure nginx
WORKDIR /app
COPY nginx.conf /etc/nginx/nginx.conf

# Create startup script
COPY start-hf.sh /app/start-hf.sh
RUN chmod +x /app/start-hf.sh

# Hugging Face Spaces requires port 7860
ENV PORT=7860
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

# Expose port 7860 (required by Hugging Face)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Start both nginx and backend
CMD ["/app/start-hf.sh"]
