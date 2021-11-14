#!/bin/bash

if [ ! -f /usr/share/fonts/material-icons/MaterialIcons-Regular.ttf ]; then
  echo "Creating directory for font material-icons"
  sudo mkdir -p /usr/share/fonts/material-icons
  echo "Downloading font material-icons"
  sudo curl https://raw.githubusercontent.com/google/material-design-icons/master/font/MaterialIcons-Regular.ttf -o /usr/share/fonts/material-icons/MaterialIcons-Regular.ttf
  echo "Installed font material-icons"
fi

if [ ! -f /usr/share/fonts/material-wifi/material-wifi.ttf ]; then
  echo "Creating directory for font material-wifi"
  sudo mkdir -p /usr/share/fonts/material-wifi
  echo "Downloading font material-wifi"
  sudo curl https://raw.githubusercontent.com/dcousens/material-wifi-icons/master/material-wifi.ttf -o /usr/share/fonts/material-wifi/material-wifi.ttf
  echo "Installed font material-wifi"
fi
