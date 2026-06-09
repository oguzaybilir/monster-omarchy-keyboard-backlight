#!/bin/bash
# Monster ABRA A5 - Clevo Klavye Arka Işık Kurulum Scripti
# Arch Linux / omarchy için

set -e

echo "==> Bağımlılıklar kontrol ediliyor..."
sudo pacman -S --needed git dkms base-devel linux-headers

echo "==> clevo-keyboard reposu indiriliyor..."
cd ~/Downloads
wget https://github.com/wessel-novacustom/clevo-keyboard/raw/master/kb.sh
chmod +x kb.sh

echo "==> Driver kuruluyor..."
sudo ./kb.sh

echo "==> Eski DKMS modülü kaldırılıp yeniden kuruluyor..."
sudo dkms remove tuxedo-keyboard/3.2.10 --all
sudo dkms install tuxedo-keyboard/3.2.10 --force

echo "==> Modüller yükleniyor..."
sudo modprobe tuxedo_keyboard
sudo modprobe clevo_acpi
sudo modprobe clevo_wmi

echo "==> Modüller kalıcı hale getiriliyor..."
echo -e "tuxedo_keyboard\nclevo_acpi\nclevo_wmi" | sudo tee /etc/modules-load.d/tuxedo.conf

echo "==> Kurulum tamamlandı! Klavye arka ışığı aktif olmalı."
echo "==> Yeniden başlatmanız önerilir: sudo reboot"