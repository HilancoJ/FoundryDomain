# Flatpak App List for Fedora Silverblue

This is a curated list of Flatpak apps, organized by category.  
Each app is listed with its **Name** and **Flatpak ID**, so it’s human-readable and script-friendly.

---

## Usage

To install all apps from this list, run the following command:

```bash
grep -oE ':[[:space:]]*\S+' flatpaks.md | sed 's/^:[[:space:]]*//' | xargs -r flatpak install -y flathub
