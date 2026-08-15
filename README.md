<div align="center">

# 🖱️ Logi Options+ (Linux GTK4 / Libadwaita) MX MASTER 3s

**A native, pixel-perfect GTK4 / Libadwaita recreation of Logitech Options+ for the Logitech MX Master 3S on Linux.**

[![License: MIT](https://img.shields.io/badge/License-MIT-00e5c9.svg?style=flat-square)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux%20%2F%20GNOME-11141c.svg?style=flat-square&logo=linux)](https://github.com/gutopardini/logi-options-gtk)
[![GUI](https://img.shields.io/badge/GUI-GTK4%20%2F%20Libadwaita-00e5c9.svg?style=flat-square&logo=gnome)](https://gtk.org)
[![Backend: logid](https://img.shields.io/badge/Backend-logiops%20%2F%20logid-white.svg?style=flat-square)](https://github.com/PixlOne/logiops)
[![i18n](https://img.shields.io/badge/i18n-English%20%7C%20Portugu%C3%AAs-blue.svg?style=flat-square)](po/)

<br/>

</div>

<img width="1379" height="850" alt="image" src="https://github.com/user-attachments/assets/42bd9960-af49-42b8-b8cd-ae2883387125" />

---

## ⚡ Instalação Rápida em 1 Linha (All-in-One One-Liner)

Instale tudo com **apenas um comando**! O instalador detecta sua distribuição Linux, instala e ativa automaticamente o daemon backend [`logiops` (`logid`)](https://github.com/PixlOne/logiops), as dependências do GTK4/Libadwaita, os catálogos de tradução, ícones e atalhos no sistema:

```bash
curl -fsSL https://raw.githubusercontent.com/gutopardini/logi-options-gtk/main/install.sh | bash
```

> **Distribuições suportadas automaticamente:** Fedora, Ubuntu, Debian, Pop!_OS, Arch Linux, Manjaro, openSUSE, Linux Mint, Zorin OS, Nobara.

---

## 🌟 Visão Geral / Overview

O **Logi Options+ para Linux** foi criado para preencher a lacuna da falta de suporte oficial da Logitech no Linux. Ele reproduz com fidelidade absoluta de **1:1** o design, as transições, os balões de chamada e o comportamento do software oficial **Logitech Options+**, integrado nativamente com o daemon [`logiops`](https://github.com/PixlOne/logiops) (`logid`), `UPower` e `Polkit`.

---

## 🌐 Internacionalização (i18n) / Multi-Language Support

O aplicativo possui suporte nativo a internacionalização via GNU Gettext e detecta automaticamente o idioma configurado no seu sistema operacional:

* 🇺🇸 **English** *(Main Language / Fonte da Verdade no Código)*
* 🇧🇷 **Português do Brasil (`pt_BR`)** *(Tradução completa 1:1)*

### Como forçar um idioma específico via terminal:
```bash
# Executar em Inglês
LANG=en_US.UTF-8 logi-options

# Executar em Português do Brasil
LANG=pt_BR.UTF-8 logi-options
```

### Como contribuir com novos idiomas (ex: Espanhol, Francês, Alemão):
1. Crie o arquivo `po/<código_idioma>.po` (ex: `po/es.po` a partir de `po/logi-options-gtk.pot`).
2. Adicione as traduções das mensagens.
3. Execute o script automatizado para compilar os catálogos:
```bash
./tools/update_translations.sh
```

---

## ✨ Principais Recursos / Key Features

### 1. 🎨 Design System & Experiência de Usuário 1:1
* **Transição Suave de Telas:** Alternância inteligente entre o **Modo Visão Geral** (mouse centralizado, balões escuros neutros, gaveta recolhida) e o **Modo Edição** (balão aceso em ciano sólido `#00e5c9`, gaveta de ações animada na direita).
* **Header Arrastável Nativo (`Gtk.WindowHandle`):** Toda a barra superior pode ser clicada e arrastada para mover a janela entre monitores ou telas. Duplo clique maximiza/restaura a janela.
* **Renders 3D Transparentes:** Imagens da visão superior e da base do MX Master 3S com canal alfa (RGBA) recortado e *feathering* suave, fundindo-se perfeitamente com o fundo escuro `#0e0f12`.
* **Ícone Oficial Multi-Resolução:** Instalado no sistema em 512x512, 256x256, 128x128, 64x64, 48x48 e 32x32.

---

### 2. 🎛️ Mapeamento Completo de Botões

| Botão | Identificador (CID) | Ações Recomendadas (Recommended) |
| :--- | :--- | :--- |
| **Wheel button** | `0x52` | `Middle button`, `Shift wheel mode`, `Task view`, `Show/hide desktop`, `Gestures`, `Keyboard shortcut` |
| **Top button** | `0xc4` | `Shift wheel mode`, `Task view`, `Middle button`, `Gestures`, `Screen capture`, `Print screen`, `Keyboard shortcut` |
| **Forward button** | `0x56` | `Forward`, `Paste` (`Ctrl+V`), `Volume up`, `Redo` (`Ctrl+Y`), `Keyboard shortcut` |
| **Back button** | `0x53` | `Back`, `Copy` (`Ctrl+C`), `Volume down`, `Undo` (`Ctrl+Z`), `Keyboard shortcut` |
| **Thumbwheel** | Horizontal Roll | `Horizontal scroll`, `Zoom in/out`, `Volume up/down`, `Navigate between tabs`, `Keyboard shortcut` |
| **Gesture button** | `0xc3` | `Gestures` (6 Presets Oficiais), `Task view`, `Show/hide desktop`, `Screen capture`, `Print screen`, `Switch application`, `Keyboard shortcut` |

---

### 3. ⌨️ Gravador de Atalhos Interativo
* **Thumbwheel Dual Recorder:** Card oficial com captura independente de teclas para **`SCROLL UP`** e **`SCROLL DOWN`** (ex: *Prnt Scrn, None*).
* **Single Button Recorder:** Captura instantânea de combinações com modificadores (`Super`, `Ctrl`, `Alt`, `Shift`).

---

### 4. 🎚️ Gestos com 6 Presets Oficiais + Custom
Card oficial de 5 direções (`← HOLD + MOVE LEFT`, `→ HOLD + MOVE RIGHT`, `↑ HOLD + MOVE UP`, `↓ HOLD + MOVE DOWN`, `○ CLICK`) com os presets:
1. 🖥️ **`Virtual desktops`** (Desktop left, Desktop right, Start menu, Show/hide desktop, Task view)
2. 🎵 **`Media controls`** (Previous, Next, Volume up, Volume down, Play/Pause)
3. 🪟 **`Windows management`** (Snap left, Snap right, Maximize window, Show/hide desktop, Switch application)
4. 🧭 **`App navigation`** (Switch app left/right, Start menu, Show/hide desktop, Switch application)
5. ✋ **`Pan`** (Pan left, right, up, down, Middle button)
6. 📐 **`Arrange windows`** (Snap left/right, Maximize, Minimize, Switch application)
7. ⚙️ **`Custom`** (Configuração livre de teclas)

---

### 5. 📂 Accordion Colapsável de `OTHER ACTIONS`
* Dicionário alfabético unificado completo (*Action center, Back, Brightness down/up, Calculator, Close window, Copy, Cut, Desktop left/right, Do nothing, Emoji menu, Forward, Input language, Lock, Maximize, Minimize, Mute, New browser tab, Next, Paste, Play/Pause, Previous, Print screen, Redo, Right Ctrl, Screen capture, Screen snip, Shift wheel mode, Show/hide desktop, Switch application, Task view, Undo, Volume down/up, Zoom in/out*).
* Expansão automática ao digitar no campo **`Search`**.

---

### 6. 📜 Apontar e Rolar (`POINT AND SCROLL`)
* **SmartShift MagSpeed:** Alternância automática entre *Ratchet* e *Free-spin* com slider de sensibilidade de 10% a 100%.
* **Thumbwheel Speed:** Calibração da velocidade de rolagem horizontal.
* **DPI Contínuo:** Ajuste óptico de precisão de **200 a 8.000 DPI**.

---

### 7. ⚡ Bateria e Aplicação no Sistema com 1 Clique
* **Leitura Real de Bateria:** Integração D-Bus com `UPower` (`85% 🔋 ⚡`).
* **Aplicação Segura com Polkit:** Botão **`Aplicar no Sistema`** autentica via janela nativa do GNOME (`pkexec`), grava em `/etc/logid.cfg` e reinicia o `logid.service` imediatamente.

---

## 📂 Estrutura do Projeto / Project Architecture

```
logi-options-gtk/
├── main.py                     # Inicializador do GTK4 / Libadwaita
├── launch.sh                   # Script de execução local
├── install.sh                  # Instalador All-in-One (Backend + GUI + Locales)
├── logi-options-gtk.desktop    # Metadados de integração no GNOME (i18n)
├── LICENSE                     # Licença MIT
├── README.md                   # Documentação do projeto
├── po/                         # 🌐 Catálogos GNU Gettext
│   ├── logi-options-gtk.pot    # Template base de strings extraídas
│   └── pt_BR.po                # Tradução em Português do Brasil
├── tools/
│   └── update_translations.sh  # Script de extração e compilação de i18n
└── app/
    ├── i18n.py                 # Módulo central de localização e fallback
    ├── window.py               # Janela principal, sidebar, header arrastável e viewstack
    ├── locale/                 # Catálogos binários compilados (.mo)
    │   └── pt_BR/LC_MESSAGES/
    │       └── logi-options-gtk.mo
    ├── assets/
    │   ├── style.css           # Design System oficial dark (#0e0f12, #00e5c9)
    │   ├── mx_master_3s.png    # Render 3D superior transparente (RGBA)
    │   └── logi-options-plus-*.png # Ícones do app (512, 256, 128, 64, 48, 32)
    ├── backend/
    │   ├── config_manager.py   # Parser e serializador do /etc/logid.cfg
    │   ├── system_service.py   # Integração D-Bus (UPower), systemd e Polkit
    │   ├── app_manager.py      # Scanner de softwares instalados (.desktop)
    │   └── keycodes.py         # Mapeamento e formatação de teclas evdev
    ├── views/
    │   ├── buttons_view.py     # Gestão 1:1 de botões, gaveta de ações e gravador
    │   ├── point_scroll_view.py# Telas de calibração MagSpeed, Thumbwheel e DPI
    │   ├── gestures_view.py    # Tela de gestos
    │   └── settings_view.py    # Informações e diagnósticos
    └── widgets/
        ├── mouse_canvas.py     # Canvas Cairo com iluminação de pins e balões
        ├── add_app_dialog.py   # Modal de seleção de softwares instalados
        ├── shortcut_recorder.py# Diálogo gravador de atalhos
        └── dpad_widget.py      # Widget da bússola de gestos
```

---

## 🛠️ Instalação Manual para Desenvolvedores

Se você prefere clonar e executar o repositório manualmente:

### 1. Dependências da GUI (GTK4 + Libadwaita):
* **Fedora:**
  ```bash
  sudo dnf install -y python3 python3-gobject gtk4 libadwaita gettext upower
  ```
* **Ubuntu / Debian:**
  ```bash
  sudo apt install -y python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gettext upower
  ```
* **Arch Linux:**
  ```bash
  sudo pacman -S python python-gobject gtk4 libadwaita gettext upower
  ```

### 2. Instalação do Backend [`logiops`](https://github.com/PixlOne/logiops):
* **Fedora:** `sudo dnf copr enable -y ruben/logiops && sudo dnf install -y logiops && sudo systemctl enable --now logid`
* **Arch Linux:** `yay -S logiops-git && sudo systemctl enable --now logid`
* **Ubuntu / Debian:** Compilar a partir de https://github.com/PixlOne/logiops

### 3. Clonar e Executar:
```bash
git clone https://github.com/gutopardini/logi-options-gtk.git
cd logi-options-gtk
./install.sh
```

---

## ⌨️ Atalhos da Interface

* **`Esc`**: Fecha a gaveta lateral de ações ou encerra o aplicativo.
* **`←`** (Header superior): Volta da gaveta de ações para o modo visão geral.
* **`✕`** (Canto superior direito): Fecha a janela.
* **Clique duplo na barra superior**: Maximiza ou restaura a janela.
* **Arrastar barra superior**: Move a janela suavemente pela tela.

---

## 📄 Licença / License

Distribuído sob a licença **MIT**. Consulte [`LICENSE`](LICENSE) para mais detalhes.

---

<div align="center">
  <sub>Desenvolvido com carinho para a comunidade Linux por <a href="https://github.com/gutopardini">Guto Pardini</a>.</sub>
</div>
