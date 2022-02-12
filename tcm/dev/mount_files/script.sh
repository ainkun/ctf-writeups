if [ -z "$(ssh-keygen -F 192.168.100.219)" ]; then
  ssh-keyscan -H 192.168.100.219 >> ~/.ssh/known_hosts
fi
