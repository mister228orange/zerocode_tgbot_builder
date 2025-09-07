FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go mod init gobotgen || true
RUN go mod tidy
RUN go build -o gobotgen main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/gobotgen /app/gobotgen
COPY state.db /app/state.db
COPY config.yaml /app/config.yaml
ENV TELEGRAM_BOT_TOKEN=""
CMD ["/app/gobotgen"]