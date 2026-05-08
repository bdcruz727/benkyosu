const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  scanOsuFolder: (folderPath) => ipcRenderer.invoke('scan-osu-folder', folderPath),
})