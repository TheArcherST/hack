#!/usr/bin/env bash
set -euo pipefail

SSH_USER="${SSH_USER:-appuser}"

# Generate host key if missing
if [ ! -f /etc/ssh/ssh_host_ed25519_key ]; then
  ssh-keygen -t ed25519 -N "" -f /etc/ssh/ssh_host_ed25519_key
fi

# Create user if not exists
if ! id "$SSH_USER" &>/dev/null; then
  useradd -m -s /usr/sbin/nologin "$SSH_USER"
fi

# Setup ~/.ssh
HOME_DIR=$(eval echo "~$SSH_USER")
mkdir -p "$HOME_DIR/.ssh"
chmod 700 "$HOME_DIR/.ssh"
chown "$SSH_USER:$SSH_USER" "$HOME_DIR/.ssh"

# ✅ Write key from ENV with strict restrictions
if [ -n "${PUBLIC_KEY:-}" ]; then
  echo "Adding authorized key from ENV"
  echo "command=\"/bin/false\",no-pty,no-agent-forwarding,no-X11-forwarding,permitopen=\"app:8000\" ${PUBLIC_KEY}" \
    > "$HOME_DIR/.ssh/authorized_keys"
  chmod 600 "$HOME_DIR/.ssh/authorized_keys"
  chown "$SSH_USER:$SSH_USER" "$HOME_DIR/.ssh/authorized_keys"
else
  echo "ERROR: No PUBLIC_KEY environment variable provided!"
  exit 1
fi

echo "Public key configured successfully"
exec "$@"
