# ⌨️ Monster Clevo Keyboard Backlight Setup

Dil / Language: [English](README.md) | [Türkçe](README.tr.md)

This tool is an automated configuration script designed to install and set up keyboard backlight drivers on **Monster Notebooks** (specifically Clevo-based Abra A5 series, etc.) running **Arch Linux** (specifically omarchy, in my case).

The setup utilizes Python's `rich` library to deliver a modern, colorized, and animated terminal user interface (complete with spinners, tables, and panels).

---

## 🚀 Features

- **Advanced Terminal UI:** Powered by the `rich` library, providing visual indicators, status checkmarks, live spinners, and a clean tabular summary.
- **Auto-Privilege Escalation:** Checks for required permissions and automatically restarts itself using `sudo` if run by a regular user.
- **Robust Error Catching:** Stops execution immediately upon any command failure, rendering error stack traces in clean, dedicated visual panels.
- **DKMS Integration:** Registers the `tuxedo-keyboard` module to DKMS, ensuring your keyboard backlight continues to work after kernel updates.
- **Persistent Modules Loading:** Automatically configures required kernel modules (`tuxedo_keyboard`, `clevo_acpi`, `clevo_wmi`) to load at system boot.
- **Safe DKMS Checkups:** Verifies whether old DKMS modules are registered before attempting to remove them, eliminating initial installation failures.

---

## 🛠️ Prerequisites

Ensure your system meets the following requirements before executing the script:
1. An **Arch Linux**-based distribution.
2. Active internet connection (to fetch drivers and dependencies).
3. User account with `sudo` privileges.

*Note: The script automatically installs missing system packages (`git`, `dkms`, `base-devel`, `linux-headers`, and `python-rich`) using `pacman`.*

---

## 📦 Installation and Usage

To run the installation script, open your terminal and follow these commands:

```bash
# Clone the repository (or download the files)
git clone https://github.com/oguzaybilir/monster-omarhy-keyboard-backlight.git
cd monster-omarhy-keyboard-backlight

# Make the wrapper script executable
chmod +x main.sh

# Run the installer
./main.sh
```

---

## 🔍 What Happens Under the Hood?

The wrapper script and installer execute the following steps in sequence:

1. **Python Environment Verification:** Checks for `python3` and `python-rich`. Installs them via `pacman` if not found.
2. **System Dependencies Installation:** Installs `git`, `dkms`, `base-devel`, and appropriate `linux-headers` for your active kernel.
3. **Fetching kb.sh:** Downloads the unofficial Clevo-keyboard setup utility script `kb.sh` from the wessel-novacustom repository.
4. **Driver Compilation:** Compiles driver code on your local machine using the downloaded utility.
5. **DKMS Registration:** Installs and registers the compiled module as `tuxedo-keyboard/3.2.10` via DKMS.
6. **Kernel Module Loading:** Loads the `tuxedo_keyboard`, `clevo_acpi`, and `clevo_wmi` modules via `modprobe`.
7. **Boot Persistence:** Writes the modules to `/etc/modules-load.d/tuxedo.conf` so they load automatically at boot.
8. **Summary Table:** Renders a clean status grid showing if each module is registered under DKMS and loaded in the kernel.

---

## ⚠️ Troubleshooting

### 1. Secure Boot Errors (Module loading failed / Required key not available)
If UEFI Secure Boot is enabled on your laptop, the kernel will refuse to load compiled third-party modules without a trusted signature.
- **Solution:** Disable Secure Boot in your BIOS configuration settings, or enroll a custom Machine Owner Key (MOK) to sign the driver modules yourself.

### 2. Missing Linux Kernel Headers
If you are running a non-standard kernel (such as `linux-lts` or `linux-zen`), standard headers will fail to build the driver.
- **Solution:** Install the specific headers package corresponding to your active kernel (obtained via `uname -r`):
  ```bash
  sudo pacman -S linux-lts-headers   # If running the LTS kernel
  sudo pacman -S linux-zen-headers   # If running the Zen kernel
  ```

### 3. Manual Status Verifications
To inspect whether modules are loaded and running properly on your system:
```bash
# Verify loaded modules
lsmod | grep tuxedo
lsmod | grep clevo

# Verify DKMS module registration
dkms status
```

---

## 👨‍💻 Contributing
If you encounter any issues or have features to submit, feel free to open a Pull Request (PR) or submit an Issue in this repository.
