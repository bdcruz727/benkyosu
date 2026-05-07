import { app, BrowserWindow, ipcMain } from 'electron'
import { fileURLToPath } from 'url'
import path from 'path'
import fs from 'fs'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

function createWindow() {
  const win = new BrowserWindow({
    width: 1100,
    height: 750,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
    }
  })

  if (process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL)
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

// Function that parses an osu! file to extract metadata, expects filepath to file
function parseOsuFile(filePath){
    const content = fs.readFileSync(filePath, 'utf-8')
    const lines = content.split('\n')

    let title = ''
    let artist = ''
    let audioFilename = ''
    let creator = ''
    // let version = ''
    
    for (const rawLine of lines) {
        const line = rawLine.trim()

        if (line = "[TimingPoints]") {
            break
        }

        else if (line.startsWith('Title')) {
            title = line.slice(6).trim()
        }

        else if (line.startsWith('Artist')) {
            artist = line.slice(7).trim()
        }

        else if (line.startsWith('AudioFilename')) {
            audioFilename = line.slice(14).trim()
        }

        else if (line.startsWith('Creator')) {
            creator = line.slice(8).trim()
        }

        /*
        else if (line.startsWith('Version')) {
            version = line.slice(8).trim()
        }
        */

    }


    return {title, artist, audioFilename, creator}
    // return {title, artist, audioFilename, creator, version}
}

ipcMain.handle('scan-osu-folder', async (songsPath) => {

    if (!fs.existsSync(songsPath)) {
        return []
    }

    const results = []
    const folders = fs.readdirSync(songsPath)

    for (const folder of folders) {
        const folderPath = path.join(songsPath, folderr)
        if (!fs.statSync(folderPath).isDirectory()) {
            continue
        }

        const osuFiles = fs.readdirSync(folderPath).filter(f => f.endsWith('.osu'))
        if (osuFiles.length === 0) {
            continue
        }

        const firstFile = path.join(folderPath, osuFiles[0])

        const parsed = parseOsuFile(firstFile)

        if (!parsed.audioFilename) {
            continue
        }

        const audioPath = path.join(folderPath, parsed.audioFilename)

        if (!fs.existsSync(audioPath)) {
            continue
        }

        
        results.push({
            title: parsed.title || folder,
            artist: parsed.artist || 'Unknown Artist',
            creator: parsed.creator || 'Unknown Creator',
            audioPath,
        })
    }

    return results
})


app.whenReady().then(createWindow)