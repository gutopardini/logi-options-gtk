<div align="center">

# 🖱️ Logi Options+ (Linux GTK4 / Libadwaita)

**A native, pixel-perfect GTK4 / Libadwaita recreation of Logitech Options+ for the Logitech MX Master 3S on Linux.**

[![License: MIT](https://img.shields.io/badge/License-MIT-00e5c9.svg?style=flat-square)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux%20%2F%20GNOME-11141c.svg?style=flat-square&logo=linux)](https://github.com/gutopardini/logi-options-gtk)
[![GTK4](https://img.shields.io/badge/GUI-GTK4%20%2F%20Libadwaita-00e5c9.svg?style=flat-square&logo=gnome)](https://gtk.org)
[![Backend: logid](https://img.shields.io/badge/Backend-logiops%20%2F%20logid-white.svg?style=flat-square)](https://github.com/PixlOne/logiops)

<br/>

</div>

---

## 🌟 Visão Geral / Overview

O **Logi Options+ para Linux** foi criado para preencher a lacuna da falta de suporte oficial da Logitech no Linux. Ele reproduz com fidelidade absoluta de **1:1** o design, as transições, os balões de chamada e o comportamento do software oficial **Logitech Options+**, integrado nativamente com o daemon [`logiops`](https://github.com/PixlOne/logiops) (`logid`), `UPower` e `Polkit`.

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

### 6. 🔄 Easy-Switch Oficial
* **Visão da Base do Mouse:** Render 3D da parte inferior do mouse com o sensor óptico Darkfield e iluminação no botão Easy-Switch.
* **Canais Pareados:** Identificação dos computadores emparelhados (*Canal 1: fedora • Bluetooth, Canal 2: Windows 11 • Bluetooth, Canal 3: No paired computer*).

---

### 7. 📜 Apontar e Rolar (`POINT AND SCROLL`)
* **SmartShift MagSpeed:** Alternância automática entre *Ratchet* e *Free-spin* com slider de sensibilidade de 10% a 100%.
* **Thumbwheel Speed:** Calibração da velocidade de rolagem horizontal.
* **DPI Contínuo:** Ajuste óptico de precisão de **200 a 8.000 DPI**.

---

### 8. ⚡ Bateria e Aplicação no Sistema com 1 Clique
* **Leitura Real de Bateria:** Integração D-Bus com `UPower` (`85% 🔋 ᛒ`).
* **Aplicação Segura com Polkit:** Botão **`Aplicar no Sistema`** autentica via janela nativa do GNOME (`pkexec`), grava em `/etc/logid.cfg` e reinicia o `logid.service` imediatamente.

---

## 📂 Estrutura do Projeto / Project Architecture

```
logi-options-gtk/
├── main.py                     # Inicializador do GTK4 / Libadwaita
├── launch.sh                   # Script de execução com resolução de caminhos
├── install.sh                  # Instalador de atalhos e ícones multi-resolução
├── logi-options-gtk.desktop    # Metadados de integração no GNOME
├── LICENSE                     # Licença MIT
├── README.md                   # Documentação do projeto
└── app/
    ├── window.py               # Janela principal, sidebar, header arrastável e viewstack
    ├── assets/
    │   ├── style.css           # Design System oficial dark (#0e0f12, #00e5c9)
    │   ├── mx_master_3s.png    # Render 3D superior transparente (RGBA)
    │   ├── mx_master_3s_base.png # Render 3D inferior (Easy-Switch) transparente
    │   └── logi-options-plus-*.png # Ícones do app (512, 256, 128, 64, 48, 32)
    ├── backend/
    │   ├── config_manager.py   # Parser e serializador do /etc/logid.cfg
    │   ├── system_service.py   # Integração D-Bus (UPower), systemd e Polkit
    │   ├── app_manager.py      # Scanner de softwares instalados (.desktop)
    │   └── keycodes.py         # Mapeamento e formatação de teclas evdev
    ├── views/
    │   ├── buttons_view.py     # Gestão 1:1 de botões, gaveta de ações e gravador
    │   ├── easy_switch_view.py # Tela da base do mouse e canais Easy-Switch
    │   ├── point_scroll_view.py# Telas de calibração MagSpeed, Thumbwheel e DPI
    │   ├── gestures_view.py    # Tela de gestos
    │   └── settings_view.py    # Informações e diagnósticos
    └── widgets/
        ├── mouse_canvas.py     # Canvas Cairo com iluminação de pins e balões
        └── add_app_dialog.py   # Modal de seleção de softwares instalados
```

---

## 🚀 Instalação e Execução / Installation

### 1. Pré-requisitos (Fedora / RHEL / Ubuntu / Debian / Arch):
* **Python 3.10+**
* **GTK4 & Libadwaita** (`python3-gobject`, `gtk4`, `libadwaita`)
* **logiops / logid** instalado e habilitado (`systemctl enable --now logid`)

No Fedora:
```bash
sudo dnf install -y python3 python3-gobject gtk4 libadwaita logiops
```

---

### 2. Clonar e Instalar:
```bash
git clone https://github.com/gutopardini/logi-options-gtk.git
cd logi-options-gtk
bash install.sh
```

---

### 3. Como Executar:
* Pelo menu de aplicativos do GNOME: Pressione **`Super`** e busque por **`Logi Options+`**.
* Pelo terminal:
```bash
logi-options
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
