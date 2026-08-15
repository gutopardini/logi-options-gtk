#!/usr/bin/env bash
# ==============================================================================
# 🖱️ Logi Options+ (Linux GTK4 / Libadwaita) - All-in-One Installer
# Suporta: Fedora, Ubuntu, Debian, Pop!_OS, Arch Linux, Manjaro, openSUSE
# Instala Backend (logiops / logid), Dependências GUI, Traduções e Atalhos
# ==============================================================================
set -e

# Cores e Estilos
BOLD='\033[1m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}${BOLD}"
echo "  __                 _    ___        _   _                   "
echo " / /   ___   __ _ (_)  /___\ _ __ | |_(_) ___  _ __  ___   "
echo "/ /   / _ \ / _\` || | //  //| '_ \| __| |/ _ \| '_ \/ __|  "
echo "/ /___| (_) | (_| || |/ \_// | |_) | |_| | (_) | | | \__ \  "
echo "\____/ \___/ \__, ||_|\___/  | .__/ \__|_|\___/|_| |_|___/  "
echo "             |___/           |_|  (GTK4 / Libadwaita)        "
echo -e "${NC}"
echo -e "${BOLD}Iniciando a instalação completa do Logi Options+...${NC}\n"

# 1. Determina Diretório de Destino
if [ -n "$BASH_SOURCE" ] && [ -f "$BASH_SOURCE" ] && [ "$(basename "$BASH_SOURCE")" != "bash" ]; then
    SRC_DIR="$(cd "$(dirname "$BASH_SOURCE")" && pwd)"
    if [ -f "$SRC_DIR/main.py" ]; then
        INSTALL_DIR="$SRC_DIR"
    else
        INSTALL_DIR="$HOME/.local/share/logi-options-gtk"
    fi
else
    INSTALL_DIR="$HOME/.local/share/logi-options-gtk"
fi

REPO_URL="https://github.com/gutopardini/logi-options-gtk.git"

# 2. Detecção de Distribuição Linux
DISTRO="unknown"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO="$ID"
    LIKE="$ID_LIKE"
fi

echo -e "🔍 Distribuição detectada: ${CYAN}${NAME:-$DISTRO}${NC}"

# Função para executar com sudo
run_sudo() {
    if [ "$EUID" -eq 0 ]; then
        "$@"
    else
        sudo "$@"
    fi
}

# 3. Instalação de Dependências e Backend logiops (logid)
echo -e "\n📦 ${BOLD}1/5: Verificando dependências do sistema e backend logiops...${NC}"

HAS_LOGID=0
if command -v logid &>/dev/null; then
    HAS_LOGID=1
fi

HAS_PYGTK=0
if python3 -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1')" &>/dev/null; then
    HAS_PYGTK=1
fi

if [ "$HAS_LOGID" -eq 1 ] && [ "$HAS_PYGTK" -eq 1 ]; then
    echo -e "   -> ${GREEN}Dependências da GUI e backend logid já estão instalados no sistema.${NC}"
else
    echo -e "   -> Instalando componentes ausentes via gerenciador de pacotes..."
    case "$DISTRO" in
        fedora|rhel|centos|nobara|almalinux|rocky)
            if [ "$HAS_PYGTK" -eq 0 ]; then
                echo -e "   -> Instalando dependências GUI (Python3, GTK4, Libadwaita, gettext)..."
                run_sudo dnf install -y python3 python3-gobject gtk4 libadwaita gettext upower git
            fi

            if [ "$HAS_LOGID" -eq 0 ]; then
                echo -e "   -> Instalando daemon logiops via COPR ruben/logiops..."
                run_sudo dnf copr enable -y ruben/logiops || true
                run_sudo dnf install -y logiops
            fi
            ;;

        ubuntu|debian|pop|linuxmint|elementary|zorin)
            run_sudo apt-get update -qq

            if [ "$HAS_PYGTK" -eq 0 ]; then
                echo -e "   -> Instalando dependências GUI (Python3, GTK4, Libadwaita, gettext)..."
                run_sudo apt-get install -y python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gettext upower git
            fi

            if [ "$HAS_LOGID" -eq 0 ]; then
                echo -e "   -> Compilando e instalando logiops do repositório oficial..."
                run_sudo apt-get install -y build-essential cmake pkg-config libevdev-dev libudev-dev libconfig++-dev
                TMP_BUILD_DIR=$(mktemp -d)
                git clone --depth 1 https://github.com/PixlOne/logiops.git "$TMP_BUILD_DIR"
                mkdir -p "$TMP_BUILD_DIR/build"
                (cd "$TMP_BUILD_DIR/build" && cmake .. && make -j"$(nproc)")
                run_sudo make -C "$TMP_BUILD_DIR/build" install
                rm -rf "$TMP_BUILD_DIR"
            fi
            ;;

        arch|manjaro|endeavouros|garuda|cachyos)
            if [ "$HAS_PYGTK" -eq 0 ]; then
                echo -e "   -> Instalando dependências GUI (Python, GTK4, Libadwaita, gettext)..."
                run_sudo pacman -S --needed --noconfirm python python-gobject gtk4 libadwaita gettext upower git
            fi

            if [ "$HAS_LOGID" -eq 0 ]; then
                if command -v yay &>/dev/null; then
                    echo -e "   -> Instalando logiops-git via AUR (yay)..."
                    yay -S --noconfirm logiops-git
                elif command -v paru &>/dev/null; then
                    echo -e "   -> Instalando logiops-git via AUR (paru)..."
                    paru -S --noconfirm logiops-git
                else
                    echo -e "${YELLOW}⚠️ Aviso: AUR helper (yay/paru) não encontrado. Por favor, instale 'logiops-git' manualmente via AUR.${NC}"
                fi
            fi
            ;;

        opensuse*|suse|tumbleweed)
            if [ "$HAS_PYGTK" -eq 0 ]; then
                echo -e "   -> Instalando dependências GUI (Python3, GTK4, Libadwaita, gettext)..."
                run_sudo zypper --non-interactive install python3 python3-gobject gtk4 libadwaita-1-0 gettext-runtime upower git
            fi
            ;;

        *)
            echo -e "${YELLOW}⚠️ Distribuição não identificada diretamente. Verifique se GTK4, Libadwaita e logiops estão instalados.${NC}"
            ;;
    esac
fi

# 4. Habilita o Serviço Systemd logid
if command -v systemctl &>/dev/null && command -v logid &>/dev/null; then
    if ! systemctl is-active --quiet logid 2>/dev/null; then
        echo -e "   -> Habilitando e iniciando o serviço systemd ${CYAN}logid.service${NC}..."
        run_sudo systemctl enable --now logid.service || true
    fi
fi

# 5. Download ou Atualização do Repositório do App
echo -e "\n📥 ${BOLD}2/5: Configurando os arquivos da aplicação...${NC}"
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.local/share/applications"
mkdir -p "$HOME/.local/share/icons/hicolor"

if [ -n "$SRC_DIR" ] && [ -f "$SRC_DIR/main.py" ]; then
    INSTALL_DIR="$SRC_DIR"
    echo -e "   -> Utilizando instalação local em: ${CYAN}$INSTALL_DIR${NC}"
else
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo -e "   -> Atualizando código existente em $INSTALL_DIR..."
        (cd "$INSTALL_DIR" && git pull --ff-only)
    else
        echo -e "   -> Clonando repositório em $INSTALL_DIR..."
        rm -rf "$INSTALL_DIR"
        git clone "$REPO_URL" "$INSTALL_DIR"
    fi
fi

# 6. Compilação das Traduções (GNU Gettext)
echo -e "\n🌐 ${BOLD}3/5: Compilando catálogos de tradução (i18n)...${NC}"
for pofile in "$INSTALL_DIR"/po/*.po; do
    if [ -f "$pofile" ]; then
        lang=$(basename "$pofile" .po)
        outdir="$INSTALL_DIR/app/locale/$lang/LC_MESSAGES"
        mkdir -p "$outdir"
        echo "   -> Compilando $lang ($outdir/logi-options-gtk.mo)..."
        msgfmt -o "$outdir/logi-options-gtk.mo" "$pofile"
    fi
done

# 7. Instalação dos Ícones Multi-Resolução
echo -e "\n🎨 ${BOLD}4/5: Instalando ícones oficiais multi-resolução...${NC}"
ASSETS_DIR="$INSTALL_DIR/app/assets"
for size in 512 256 128 64 48 32; do
    mkdir -p "$HOME/.local/share/icons/hicolor/${size}x${size}/apps"
    if [ -f "$ASSETS_DIR/logi-options-plus-${size}.png" ]; then
        cp "$ASSETS_DIR/logi-options-plus-${size}.png" "$HOME/.local/share/icons/hicolor/${size}x${size}/apps/logi-options-plus.png"
        cp "$ASSETS_DIR/logi-options-plus-${size}.png" "$HOME/.local/share/icons/hicolor/${size}x${size}/apps/io.github.pixlone.logioptions.gtk.png"
    fi
done

# 8. Criação do Atalho Desktop e Executável
echo -e "\n🚀 ${BOLD}5/5: Criando executável e atalho no GNOME...${NC}"

# Script executável standalone em ~/.local/bin/logi-options
cat << EOF > "$HOME/.local/bin/logi-options"
#!/usr/bin/env bash
exec python3 "$INSTALL_DIR/main.py" "\$@"
EOF
chmod +x "$HOME/.local/bin/logi-options"
chmod +x "$INSTALL_DIR/launch.sh" "$INSTALL_DIR/main.py" "$INSTALL_DIR/install.sh"

# Atalho oficial .desktop
cat << EOF > "$HOME/.local/share/applications/io.github.pixlone.logioptions.gtk.desktop"
[Desktop Entry]
Name=Logi Options+
Comment=Logitech Options+ for Linux (MX Master 3S)
Comment[pt_BR]=Logitech Options+ oficial para Linux (MX Master 3S)
Exec=$HOME/.local/bin/logi-options
Icon=io.github.pixlone.logioptions.gtk
Terminal=false
Type=Application
Categories=Settings;HardwareSettings;Utility;GTK;
StartupWMClass=io.github.pixlone.logioptions.gtk
Keywords=logitech;options;mouse;mx;master;3s;bluetooth;settings;
EOF

# Atualiza caches do sistema
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true

echo -e "\n${GREEN}${BOLD}══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  ✅ Logi Options+ instalado e configurado com sucesso!${NC}"
echo -e "${GREEN}${BOLD}══════════════════════════════════════════════════════════════${NC}\n"
echo -e "📌 ${BOLD}Como executar:${NC}"
echo -e "   • Pelo menu de aplicativos: busque por ${CYAN}Logi Options+${NC}"
echo -e "   • Pelo terminal: execute ${CYAN}logi-options${NC}\n"
echo -e "🌐 ${BOLD}Idiomas suportados:${NC}"
echo -e "   • English (Default) | Português do Brasil (pt_BR)"
echo -e "   • Detecção automática pelo idioma do sistema operacional!\n"
