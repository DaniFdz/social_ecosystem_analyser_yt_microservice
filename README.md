# TFG

## Setup CI/CD
```bash
# Create ssh key and add it to folder ~/.ssh/authorized_keys
ssh-keygen -t rsa -b 4096 -f ~/.ssh/droplet_tfg
cat ~/.ssh/droplet_tfg.pub

ssh root@<ip> -i ~/.ssh/droplet_tfg
###
# Create a key to clone the repo from github and it to personal ssh-keys
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub

# Install dependencies

# Update the package index and upgrade packages
sudo apt update -y && sudo apt upgrade -y

# Install packages
sudo apt install -y git

# Add Docker's official GPG key:
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa

# Install python and poetry
sudo apt update -y
sudo apt install python3.11 pipx
pipx install poetry

mkdir ~/.yt_service

# Exit then ssh back in to pick up new permissions
exit
ssh root@<ip> -i ~/.ssh/droplet_tfg
```

## Installation

### Install [🤖 Just](https://github.com/casey/just) and [🌐 Poetry](https://python-poetry.org/)

```bash
sudo apt install cargo pipx
cargo install just
pipx install poetry
```

### Add cargo bin to path

Add this line to your .bashrc or .zshrc

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

Install dependencies
```bash
just install
```
