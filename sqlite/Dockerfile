FROM alpine:3.17

RUN apk add --no-cache sqlite

WORKDIR /app

COPY ./data /app/data

EXPOSE 8080

CMD ["tail", "-f", "/dev/null"]
