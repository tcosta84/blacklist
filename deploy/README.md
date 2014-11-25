# Deploy

An Ansible Playbook for quickly deploying this app on CentOS.

## Requirements

### Ansible (v1.6.10)

#### Installation

##### Ubuntu
    
    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible

##### Mac
    
    brew update
    brew install ansible

### SSHPass (v.1.05)

#### Installation

##### Ubuntu

    sudo apt-get install sshpass

##### Mac

    cd ~/Downloads
    curl -O -L http://downloads.sourceforge.net/project/sshpass/sshpass/1.05/sshpass-1.05.tar.gz
    tar xvzf sshpass-1.05.tar.gz
    cd sshpass-1.05

    ./configure
    make
    sudo make install

## Getting Started

### Install requirements:

    ansible-galaxy install -r requirements.txt

### Run playbook:

    ansible-playbook -i hosts/{{env}} site.yml --ask-pass

## Deployment key

Pay attention to the "djangoapp_repo_deploy_key" setting.
When deploying this app, you will have to create your own deployment key on Stash.

More info about deployment keys below:

https://confluence.atlassian.com/display/BITBUCKET/Use+deployment+keys
