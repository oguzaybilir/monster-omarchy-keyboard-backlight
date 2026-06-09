#!/bin/bash
# Monster ABRA A5 - Clevo Klavye Arka Işık Kurulum Scripti (Wrapper)
# Arch Linux / omarchy için

set -e

# Renk tanımlamaları
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # Renk yok

echo -e "${BLUE}==>${NC} Python ortamı kontrol ediliyor..."

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}==>${NC} Python3 bulunamadı, kuruluyor..."
    sudo pacman -S --needed --noconfirm python
fi

# python-rich kütüphanesi kontrolü
if ! python3 -c "import rich" &> /dev/null; then
    echo -e "${YELLOW}==>${NC} 'python-rich' kütüphanesi bulunamadı, pacman ile kuruluyor..."
    sudo pacman -S --needed --noconfirm python-rich
fi

# Çalışma dizinini scriptin bulunduğu dizin olarak ayarlayalım
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# setup.py dosyasına çalıştırma izni verelim
chmod +x setup.py

# Python kurulum scriptini çalıştıralım
echo -e "${GREEN}==>${NC} Görsel arayüz başlatılıyor..."
exec sudo python3 setup.py