FROM redis:6.2-alpine

# Load environment variables from the .env file
ENV REDIS_PASS=${REDIS_PASS}

# Expose Redis default port
EXPOSE 6379

# Command to run Redis server with password protection and AOF enabled
CMD ["redis-server", "--requirepass", "${REDIS_PASS}", "--appendonly", "yes"]
