FROM debian:stable-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      openssh-server ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# create unprivileged user; home for authorized_keys
ARG SSH_USER=appuser
RUN useradd -m -s /usr/sbin/nologin ${SSH_USER} && \
    mkdir -p /home/${SSH_USER}/.ssh /var/run/sshd && \
    chown -R ${SSH_USER}:${SSH_USER} /home/${SSH_USER}/.ssh && \
    chmod 700 /home/${SSH_USER}/.ssh

# host keys generated at container start
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY sshd_config /etc/ssh/sshd_config

# hardened config provided by bind-mount in compose
EXPOSE 22
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/usr/sbin/sshd","-D","-e"]
