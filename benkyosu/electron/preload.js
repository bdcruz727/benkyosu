import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  scanOsuFolder: (folderPath) => ipcRenderer.invoke('scan-osu-folder', folderPath),
})