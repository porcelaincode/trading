FROM rabbitmq:3.9-management-alpine

# Load environment variables from the .env file
ENV RABBITMQ_USER=${RABBITMQ_USER}
ENV RABBITMQ_PASS=${RABBITMQ_PASS}
ENV RABBITMQ_HOST=${RABBITMQ_HOST}
ENV RABBITMQ_PORT=${RABBITMQ_PORT}

# Expose RabbitMQ default ports
EXPOSE 5672 15672

# Command to run RabbitMQ server
CMD ["rabbitmq-server"]
