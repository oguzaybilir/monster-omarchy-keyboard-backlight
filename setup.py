#!/usr/bin/env python3
import os
import sys
import subprocess
import urllib.request
import pwd
from pathlib import Path

# Ensure the script is run with sudo (root privileges)
if os.geteuid() != 0:
    print("This script requires root privileges. Re-running with sudo...")
    try:
        args = ["sudo", sys.executable] + sys.argv
        os.execvp("sudo", args)
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")
        sys.exit(1)

# Import rich (guaranteed to be installed by the wrapper script main.sh)
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.status import Status
    from rich.table import Table
    from rich.text import Text
    from rich.align import Align
except ImportError:
    print("Error: 'rich' library is missing. Please run main.sh instead of executing setup.py directly.")
    sys.exit(1)

console = Console()

def get_real_user_details():
    """Get the username and home directory of the actual user who invoked sudo."""
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user:
        try:
            pw = pwd.getpwnam(sudo_user)
            return sudo_user, Path(pw.pw_dir)
        except KeyError:
            pass
    
    # Fallback to current user (root)
    user = os.environ.get('USER') or 'root'
    return user, Path(os.path.expanduser("~"))

def run_command(cmd, shell=False, check=True):
    """Run a system command and return output. Raises subprocess.CalledProcessError if check=True and command fails."""
    result = subprocess.run(
        cmd,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, output=result.stdout, stderr=result.stderr
        )
    return result

def is_dkms_installed(module_name, version):
    """Check if a specific DKMS module is registered."""
    try:
        res = run_command(["dkms", "status"], check=False)
        return f"{module_name}/{version}" in res.stdout
    except Exception:
        return False

def get_module_load_status(module_name):
    """Check if a kernel module is currently loaded."""
    try:
        # Check /proc/modules
        with open("/proc/modules", "r") as f:
            modules = f.read()
        return module_name in modules
    except Exception:
        return False

def print_welcome():
    welcome_text = Text()
    welcome_text.append("Monster Notebook - Clevo Klavye Arka Işık Kurulumu\n", style="bold cyan")
    welcome_text.append("Arch Linux / tuxedo-keyboard ve clevo modülleri için tasarlanmıştır.", style="italic grey70")
    
    panel = Panel(
        Align.center(welcome_text),
        border_style="cyan",
        title="[bold white]OMARCHY Keyboard Backlight Setup[/bold white]",
        subtitle="[cyan]v1.0.0[/cyan]",
        padding=(1, 2)
    )
    console.print(panel)
    console.print()

def main():
    print_welcome()
    
    real_user, real_home = get_real_user_details()
    downloads_dir = real_home / "Downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    kb_script_path = downloads_dir / "kb.sh"
    
    # Step 1: Pacman dependencies
    with console.status("[bold blue]Bağımlılıklar kontrol ediliyor ve kuruluyor... (pacman)", spinner="dots") as status:
        try:
            packages = ["git", "dkms", "base-devel", "linux-headers"]
            # Run pacman --needed
            run_command(["pacman", "-S", "--needed", "--noconfirm"] + packages)
            console.print("[green]✔[/green] Bağımlı paketler hazır (git, dkms, base-devel, linux-headers).")
        except subprocess.CalledProcessError as e:
            console.print("[red]✘ Bağımlılıklar kurulamadı![/red]")
            console.print(Panel(e.stderr, title="Hata Detayları", border_style="red"))
            sys.exit(1)

    # Step 2: Download kb.sh
    with console.status("[bold blue]Clevo-keyboard scripti indiriliyor (kb.sh)...", spinner="dots") as status:
        try:
            url = "https://github.com/wessel-novacustom/clevo-keyboard/raw/master/kb.sh"
            urllib.request.urlretrieve(url, kb_script_path)
            kb_script_path.chmod(0o755)
            console.print(f"[green]✔[/green] clevo-keyboard scripti indirildi: [yellow]{kb_script_path}[/yellow]")
        except Exception as e:
            console.print("[red]✘ Script indirilemedi![/red]")
            console.print(Panel(str(e), title="Hata Detayları", border_style="red"))
            sys.exit(1)

    # Step 3: Run kb.sh driver setup
    with console.status("[bold blue]Klavye sürücüsü derleniyor ve kuruluyor (kb.sh)...", spinner="dots") as status:
        try:
            # Run kb.sh. Note: kb.sh needs to be run in its target directory or run absolute path
            # We change Cwd to downloads_dir to mimic 'cd ~/Downloads && ./kb.sh'
            result = subprocess.run(
                [str(kb_script_path)],
                cwd=str(downloads_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, "kb.sh", output=result.stdout, stderr=result.stderr
                )
            console.print("[green]✔[/green] Sürücü başarıyla kuruldu.")
        except subprocess.CalledProcessError as e:
            console.print("[red]✘ Sürücü kurulumu başarısız![/red]")
            console.print(Panel(e.stderr or e.output, title="kb.sh Hata Detayları", border_style="red"))
            sys.exit(1)

    # Step 4: DKMS module management
    # Remove old dkms module if present
    module_name = "tuxedo-keyboard"
    module_version = "3.2.10"
    
    if is_dkms_installed(module_name, module_version):
        with console.status(f"[bold blue]Eski DKMS modülü kaldırılıyor ({module_name}/{module_version})...", spinner="dots") as status:
            try:
                run_command(["dkms", "remove", f"{module_name}/{module_version}", "--all"])
                console.print(f"[green]✔[/green] Eski DKMS modülü kaldırıldı.")
            except subprocess.CalledProcessError as e:
                console.print(f"[yellow]⚠ Eski DKMS modülü kaldırılırken uyarı/hata oluştu (Devam ediliyor):[/yellow]")
                console.print(Panel(e.stderr, title="DKMS Kaldırma Uyarısı", border_style="yellow"))
    else:
        console.print(f"[blue]ℹ[/blue] Eski dkms modülü bulunamadı ({module_name}/{module_version}), kaldırma adımı atlandı.")

    # Install DKMS module
    with console.status(f"[bold blue]DKMS modülü yeniden kuruluyor ({module_name}/{module_version})...", spinner="dots") as status:
        try:
            run_command(["dkms", "install", f"{module_name}/{module_version}", "--force"])
            console.print(f"[green]✔[/green] DKMS modülü kuruldu.")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]✘ DKMS modülü kurulumu başarısız![/red]")
            console.print(Panel(e.stderr, title="DKMS Kurulum Hatası", border_style="red"))
            sys.exit(1)

    # Step 5: Load kernel modules
    modules_to_load = ["tuxedo_keyboard", "clevo_acpi", "clevo_wmi"]
    loaded_status = {}
    
    with console.status("[bold blue]Çekirdek modülleri yükleniyor (modprobe)...", spinner="dots") as status:
        for mod in modules_to_load:
            try:
                run_command(["modprobe", mod])
                loaded_status[mod] = True
            except subprocess.CalledProcessError as e:
                loaded_status[mod] = False
                console.print(f"[yellow]⚠ Modül yüklenemedi: {mod}[/yellow]")
    
    # Step 6: Persist modules (write to /etc/modules-load.d/tuxedo.conf)
    with console.status("[bold blue]Modüller başlangıç için kalıcı hale getiriliyor...", spinner="dots") as status:
        try:
            conf_path = Path("/etc/modules-load.d/tuxedo.conf")
            conf_path.parent.mkdir(parents=True, exist_ok=True)
            content = "\n".join(modules_to_load) + "\n"
            conf_path.write_text(content)
            console.print(f"[green]✔[/green] Modüller başlangıç listesine eklendi: [yellow]{conf_path}[/yellow]")
        except Exception as e:
            console.print("[red]✘ Modüller kalıcı hale getirilemedi![/red]")
            console.print(Panel(str(e), title="Hata Detayları", border_style="red"))
            sys.exit(1)

    # Display Final Status Table
    console.print()
    table = Table(title="Sürücü ve Modül Durumları", border_style="cyan")
    table.add_column("Modül Adı", style="bold white")
    table.add_column("DKMS Durumu", style="cyan")
    table.add_column("Yüklenme Durumu", style="green")
    
    for mod in modules_to_load:
        dkms_ok = "[green]Yüklü[/green]" if is_dkms_installed("tuxedo-keyboard", "3.2.10") and mod == "tuxedo_keyboard" else "[grey50]N/A[/grey50]"
        is_loaded = get_module_load_status(mod)
        load_ok = "[green]Aktif (Loaded)[/green]" if is_loaded else "[red]Pasif (Not Loaded)[/red]"
        table.add_row(mod, dkms_ok, load_ok)
        
    console.print(table)
    console.print()
    
    # Final message
    success_text = Text()
    success_text.append("Kurulum tamamlandı! Klavye arka ışığı şu an aktif olmalıdır.\n\n", style="bold green")
    success_text.append("Değişikliklerin kararlı çalışması için bilgisayarınızı yeniden başlatmanız önerilir:\n", style="white")
    success_text.append("sudo reboot", style="bold yellow")
    
    success_panel = Panel(
        Align.center(success_text),
        border_style="green",
        title="[bold green]✓ BAŞARILI[/bold green]",
        padding=(1, 2)
    )
    console.print(success_panel)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]İşlem kullanıcı tarafından iptal edildi.[/red]")
        sys.exit(1)
