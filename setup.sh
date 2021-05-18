#!/usr/bin/zsh
if [ -z "$1" ]
then
  echo "Please sepecify directory"
else
    sudo mkdir $1
    sudo mkdir $1/response
    sudo mkdir $1/success
    sudo mkdir $1/fail
    sudo mkdir $1/callback_ok
    sudo mkdir $1/callback_fail
    sudo chmod go+rwx $1
    sudo chmod go+rwx $1/response
    sudo chmod go+rwx $1/success
    sudo chmod go+rwx $1/fail
    sudo chmod go+rwx $1/callback_ok
    sudo chmod go+rwx $1/callback_fail
fi
