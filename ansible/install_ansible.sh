#!/bin/bash

# Установка python3
sudo apt-get install python3 -y

# Установка python3-pip
sudo apt install python3-pip -y

# Установка sshpass
sudo apt install sshpass

# Установка Ansible
pip3 install ansible

# Добавление пути к исполняемым файлам Ansible в переменную PATH
echo 'export PATH=$PATH:$HOME/.local/bin' >> $HOME/.bashrc

# Создание каталога для инвентарного файла
mkdir -p $HOME/MyPythonBot/ansible

# Создание конфигурационного файла Ansible
cat <<EOF > $HOME/MyPythonBot/ansible/ansible.cfg
[defaults]
inventory = $HOME/MyPythonBot/ansible/inventory
host_key_checking = false
EOF

echo "Установка и настройка Ansible завершена."

# Запуск основного Ansible
ansible-playbook $HOME/MyPythonBot/ansible/playbook_tg_bot.yml --ask-become-pass