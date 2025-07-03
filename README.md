# 📡 Wireless Network Visualisation Tool

This Python tool lets you map wireless network performance across a physical site using a site map image and CSV data. It overlays coloured, semi-transparent circles on top of your image to indicate the relative connection speed at various locations.

Useful for:
- 📍 Site surveys
- 🛠 Network planning
- 🧪 Signal strength analysis

---

## 🔧 Features

- Load your site map image (JPG/PNG)
- Click to place markers for each location
- CSV-driven input for up/down speeds
- Automatically colour-coded markers (red = slow, green = fast)
- Interactive map with hoverable tooltips showing speed data

---

## 📁 Example Input

### CSV format

```csv
Lobby,10,50
Office A,5,20
Server Room,100,200
Reception,15,30
