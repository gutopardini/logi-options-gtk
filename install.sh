#!/usr/bin/env bash
# Script de Instalação do Logi Options+ (Linux GTK4 / Libadwaita)
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$APP_DIR/app/assets"

echo "📦 Instalando Logi Options+ e ícone oficial no sistema..."

# 1. Cria diretórios de usuário
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.local/share/applications"

# Diretórios de Ícones
for size in 512x512 256x256 128x128 64x64 48x48 32x32; do
  mkdir -p "$HOME/.local/share/icons/hicolor/$size/apps"
done

# Remove qualquer SVG antigo do cache
rm -f "$HOME/.local/share/icons/hicolor/scalable/apps/io.github.pixlone.logioptions.gtk.svg"
rm -f "$HOME/.local/share/icons/hicolor/scalable/apps/logi-options-plus.svg"

# 2. Instala os ícones oficiais PNG em todas as resoluções
for size in 512 256 128 64 48 32; do
  if [ -f "$ASSETS_DIR/logi-options-plus-${size}.png" ]; then
    cp "$ASSETS_DIR/logi-options-plus-${size}.png" "$HOME/.local/share/icons/hicolor/${size}x${size}/apps/logi-options-plus.png"
    cp "$ASSETS_DIR/logi-options-plus-${size}.png" "$HOME/.local/share/icons/hicolor/${size}x${size}/apps/io.github.pixlone.logioptions.gtk.png"
  fi
done

# 3. Cria script executável standalone em ~/.local/bin/logi-options
rm -f "$HOME/.local/bin/logi-options"
cat << EOF > "$HOME/.local/bin/logi-options"
#!/usr/bin/env bash
exec python3 "$APP_DIR/main.py" "\$@"
EOF
chmod +x "$HOME/.local/bin/logi-options"
chmod +x "$APP_DIR/launch.sh" "$APP_DIR/main.py" "$APP_DIR/install.sh"

# 4. Instala o atalho de aplicativo oficial do GNOME
rm -f "$HOME/.local/share/applications/logi-options-gtk.desktop"
cat << EOF > "$HOME/.local/share/applications/io.github.pixlone.logioptions.gtk.desktop"
[Desktop Entry]
Name=Logi Options+
Comment=Logitech Options+ oficial para Linux (MX Master 3S)
Exec=$APP_DIR/launch.sh
Icon=io.github.pixlone.logioptions.gtk
Terminal=false
Type=Application
Categories=Settings;HardwareSettings;Utility;GTK;
StartupWMClass=io.github.pixlone.logioptions.gtk
Keywords=logitech;options;mouse;mx;master;3s;bluetooth;settings;
EOF

# 5. Atualiza os caches de ícones e do GNOME
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true

echo "✅ Logi Options+ instalado e configurado com sucesso!"
