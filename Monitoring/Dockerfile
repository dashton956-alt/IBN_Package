FROM balabit/syslog-ng:latest

# Install additional dependencies for Kafka support
USER root

# Install necessary packages
RUN apk add --no-cache \
    librdkafka \
    librdkafka-dev \
    curl \
    bash

# Create necessary directories
RUN mkdir -p /var/log/syslog-ng /etc/syslog-ng/templates

# Set permissions
RUN chown -R syslog-ng:syslog-ng /var/log/syslog-ng

USER syslog-ng

EXPOSE 514/udp 514/tcp 601/tcp

CMD ["/usr/sbin/syslog-ng", "-F", "-f", "/etc/syslog-ng/syslog-ng.conf"]
