#!/bin/bash

VM_NAME="ubuntu-cloud-vm"
VM_DIR="$HOME/$VM_NAME"
UBUNTU_CLOUD_IMAGE_URL="https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
CLOUD_IMAGE_BASENAME=$(basename "$UBUNTU_CLOUD_IMAGE_URL")
PRIMARY_DISK_IMAGE="$VM_DIR/$VM_NAME.qcow2"
CLOUD_INIT_SEED_IMAGE="$VM_DIR/cidata.iso"
VM_RAM="2048" # MB
VM_CPUS="2"
VM_DISK_SIZE="20G" 
SSH_FORWARD_PORT="2222"
DEFAULT_USER="ubuntu"
DEFAULT_USER_PASSWORD="ubuntu"

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: '$1' is not installed."
        echo "Please install it using your distribution's package manager. For Ubuntu/Debian:"
        echo "  sudo apt update"
        echo "  sudo apt install $2"
        exit 1
    fi
}

generate_ssh_key() {
    SSH_KEY_PATH="$HOME/.ssh/id_rsa"
    if [ ! -f "$SSH_KEY_PATH" ]; then
        echo "SSH key not found at $SSH_KEY_PATH. Generating a new one..."
        ssh-keygen -t rsa -b 4096 -f "$SSH_KEY_PATH" -N ""
        echo "SSH key generated."
    else
        echo "Existing SSH key found at $SSH_KEY_PATH. Using it."
    fi
    
    SSH_PUBLIC_KEY=$(cat "${SSH_KEY_PATH}.pub")
    if [ -z "$SSH_PUBLIC_KEY" ]; then
        echo "Error: Could not read SSH public key from ${SSH_KEY_PATH}.pub"
        exit 1
    fi
}

cleanup() {
    echo "Cleaning up VM files in $VM_DIR..."
    rm -rf "$VM_DIR"
    echo "Cleanup complete."
    exit 0
}

echo "--- QEMU Ubuntu Cloud Image Setup Script ---"

if [[ "$1" == "cleanup" ]]; then
    cleanup
fi

echo "Checking for required tools..."
check_command "qemu-system-x86_64" "qemu-system-x86"
check_command "cloud-localds" "cloud-image-utils"
check_command "genisoimage" "genisoimage"
check_command "wget" "wget"
echo "All required tools are installed."

if [ -d "$VM_DIR" ]; then
    read -p "Directory $VM_DIR already exists. Do you want to remove it and start fresh? (y/N): " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf "$VM_DIR"
        echo "Removed existing directory."
    else
        echo "Aborting to prevent data loss. Please choose a different VM_NAME or clean up manually."
        exit 1
    fi
fi

mkdir -p "$VM_DIR"
echo "Created VM directory: $VM_DIR"
cd "$VM_DIR" || { echo "Failed to change directory to $VM_DIR"; exit 1; }

if [ ! -f "$CLOUD_IMAGE_BASENAME" ]; then
    echo "Downloading Ubuntu Cloud Image ($UBUNTU_CLOUD_IMAGE_URL)..."
    wget "$UBUNTU_CLOUD_IMAGE_URL" -O "$CLOUD_IMAGE_BASENAME"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download cloud image."
        exit 1
    fi
else
    echo "Ubuntu Cloud Image already exists locally: $CLOUD_IMAGE_BASENAME"
fi

if [ ! -f "$PRIMARY_DISK_IMAGE" ]; then
    echo "Creating primary VM disk image ($PRIMARY_DISK_IMAGE) with backing file..."
    qemu-img create -f qcow2 -o backing_file="$CLOUD_IMAGE_BASENAME",backing_fmt=qcow2 "$PRIMARY_DISK_IMAGE" "$VM_DISK_SIZE"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create primary disk image."
        exit 1
    fi
else
    echo "Primary VM disk image already exists: $PRIMARY_DISK_IMAGE"
fi

generate_ssh_key

echo "Creating cloud-init configuration files..."

cat <<EOF > user-data
#cloud-config
hostname: $VM_NAME
manage_etc_hosts: true
users:
  - name: $DEFAULT_USER
    lock_passwd: false
    ssh_authorized_keys:
      - $SSH_PUBLIC_KEY
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: sudo
    shell: /bin/bash
chpasswd:
  list: |
    $DEFAULT_USER:$DEFAULT_USER_PASSWORD
  expire: False
ssh_pwauth: True # Allow password authentication (for initial setup, SSH keys are preferred)

package_update: true
packages:
  - qemu-guest-agent
  - curl
  - git

runcmd:
  - echo "Cloud-init setup complete for $VM_NAME!" > /var/log/cloud-init-status.txt
  - echo "You can log in via SSH using: ssh -p $SSH_FORWARD_PORT $DEFAULT_USER@localhost" >> /var/log/cloud-init-status.txt
EOF

cat <<EOF > meta-data
instance-id: $(uuidgen || echo "i-$(date +%s)")
local-hostname: $VM_NAME
EOF

echo "Cloud-init files created."

echo "Creating cloud-init seed image ($CLOUD_INIT_SEED_IMAGE)..."
genisoimage -output "$CLOUD_INIT_SEED_IMAGE" -volid cidata -rational-rock -joliet user-data meta-data
if [ $? -ne 0 ]; then
    echo "Error: Failed to create cloud-init seed image."
    exit 1
fi
echo "Cloud-init seed image created."

echo "Launching QEMU VM '$VM_NAME'..."

QEMU_CMD="qemu-system-x86_64 \
  -enable-kvm \
  -m $VM_RAM \
  -smp $VM_CPUS \
  -name $VM_NAME \
  -nographic \
  -netdev user,id=net0,hostfwd=tcp::$SSH_FORWARD_PORT-:22 \
  -device virtio-net-pci,netdev=net0 \
  -drive if=virtio,format=qcow2,file=$PRIMARY_DISK_IMAGE \
  -drive if=virtio,format=raw,file=$CLOUD_INIT_SEED_IMAGE,media=cdrom"

$QEMU_CMD

echo ""
echo "--- QEMU VM '$VM_NAME' has exited ---"
echo "  ssh -p $SSH_FORWARD_PORT $DEFAULT_USER@localhost"
echo "If you want to clean up all files created by this script, run:"
echo "  bash $(basename "$0") cleanup"
echo ""
