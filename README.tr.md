# ⌨️ Monster Clevo Keyboard Backlight Setup

Dil / Language: [English](README.md) | [Türkçe](README.tr.md)

Bu araç, **Monster Notebook** (özellikle Clevo kasalı Abra A5 serileri vb.) bilgisayarlarda **Arch Linux** (benim senaryomda omarchy) üzerinde klavye arka ışık sürücüsünü kurmak ve yapılandırmak için geliştirilmiş otomatik bir kurulum scriptidir.

Kurulum işlemi Python'ın `rich` kütüphanesi kullanılarak tasarlanmış, terminalde modern, renkli ve animasyonlu (spinner'lar, tablolar ve paneller) bir görsel deneyim sunar.

---

## 🚀 Özellikler

- **Gelişmiş Terminal Arayüzü:** `rich` kütüphanesi desteğiyle yükleme adımlarını dinamik spinner'lar, renkli checkmark'lar ve durumu gösteren tablolar ile sunar.
- **Akıllı Yetki Yönetimi (Auto-Elevate):** Script normal kullanıcı olarak başlatılsa dahi gerekli adımlarda yetkileri kontrol eder ve kendisini otomatik olarak `sudo` ile yeniden başlatır.
- **Gelişmiş Hata Yakalama:** Herhangi bir adımda hata oluşması durumunda süreci durdurup hata ayrıntılarını paneller içinde temiz bir şekilde raporlar.
- **DKMS Entegrasyonu:** `tuxedo-keyboard` modülü DKMS aracılığıyla kurulur, böylece Arch Linux çekirdek güncellemelerinden sonra klavye ışığınız çalışmaya devam eder.
- **Kalıcı Ayarlar:** Sistem başlangıcında klavye modüllerinin (`tuxedo_keyboard`, `clevo_acpi`, `clevo_wmi`) otomatik yüklenmesini sağlar.
- **Akıllı DKMS Kontrolü:** Eski DKMS modüllerini kaldırırken sistemde yüklü olup olmadıklarını önce denetler, böylece ilk kurulumda gereksiz hata alınmasını önler.

---

## 🛠️ Ön Gereksinimler

Kurulumu yapmadan önce sisteminizde aşağıdakilerin olduğundan emin olun:
1. **Arch Linux** tabanlı bir dağıtım.
2. İnternet bağlantısı (sürücüleri ve kütüphaneleri indirmek için).
3. `sudo` yetkisine sahip bir kullanıcı.

*Not: Script, bağımlılıkları (`git`, `dkms`, `base-devel`, `linux-headers` ve `python-rich`) otomatik olarak `pacman` aracılığıyla kuracaktır.*

---

## 📦 Kurulum ve Kullanım

Scripti çalıştırmak için terminali açıp aşağıdaki adımları takip edin:

```bash
# Depoyu klonlayın (veya dosyaları indirin)
git clone https://github.com/oguzaybilir/monster-omarhy-keyboard-backlight.git
cd monster-omarhy-keyboard-backlight

# Scripti çalıştırılabilir yapın
chmod +x main.sh

# Scripti başlatın
./main.sh
```

---

## 🔍 Arka Planda Ne Yapılıyor?

Script sırasıyla şu adımları gerçekleştirir:

1. **Bağımlılık Kontrolü:** `python3` ve `python-rich` paketlerinin kurulu olup olmadığını denetler. Eksikse `pacman` ile otomatik kurar.
2. **Paket Güncelleme/Yükleme:** Sistemde sürücü derlemek için gerekli olan `git`, `dkms`, `base-devel` ve aktif kernel yapınıza uygun `linux-headers` paketlerini kurar.
3. **kb.sh İndirme:** Clevo klavyeler için geliştirilen resmi olmayan `kb.sh` kurulum betiğini wessel-novacustom reposundan indirir.
4. **Sürücü Derleme:** `kb.sh` yardımıyla sürücü dosyalarını yerel bilgisayarınızda derler.
5. **DKMS Kaydı:** Derlenen `tuxedo-keyboard/3.2.10` modülünü dkms sistemine kaydeder.
6. **Modül Yükleme:** `tuxedo_keyboard`, `clevo_acpi` ve `clevo_wmi` modüllerini `modprobe` ile çekirdeğe yükler.
7. **Modülleri Kalıcı Yapma:** `/etc/modules-load.d/tuxedo.conf` dosyasına modülleri yazarak her açılışta otomatik aktif olmalarını sağlar.
8. **Özet Tablo:** Kurulum bittiğinde hangi modülün dkms durumunun ne olduğunu ve aktif olarak çekirdeğe yüklenip yüklenmediğini gösteren şık bir tablo bastırır.

---

## ⚠️ Sorun Giderme (Troubleshooting)

### 1. Secure Boot Hatası (Modül yüklenemedi uyarısı)
Eğer sisteminizde UEFI Secure Boot aktifse, derlenen üçüncü parti çekirdek modülleri yüklenirken `Required key not available` hatası alabilirsiniz.
- **Çözüm:** Secure Boot'u BIOS ayarlarından kapatın veya kendi MOK (Machine Owner Key) anahtarınızı oluşturup modülü imzalayın.

### 2. Linux Headers Eksikliği
Eğer özel bir kernel (örneğin `linux-lts`, `linux-zen`) kullanıyorsanız standart `linux-headers` paketi yerine kendi kernel'ınıza uygun başlık dosyalarını kurmanız gerekir.
- **Çözüm:** `uname -r` çıktısına uygun headers paketini kurun:
  ```bash
  sudo pacman -S linux-lts-headers   # LTS kernel kullanıyorsanız
  sudo pacman -S linux-zen-headers   # Zen kernel kullanıyorsanız
  ```

### 3. Durum Kontrolü
Modüllerin başarıyla yüklenip yüklenmediğini kendiniz kontrol etmek isterseniz:
```bash
# Modüller yüklü mü?
lsmod | grep tuxedo
lsmod | grep clevo

# DKMS durumunu kontrol edin
dkms status
```

---

## 👨‍💻 Katkıda Bulunma
Herhangi bir hata ile karşılaşırsanız veya bir özellik eklemek isterseniz PR (Pull Request) açabilir ya da Issue üzerinden bildirebilirsiniz.
