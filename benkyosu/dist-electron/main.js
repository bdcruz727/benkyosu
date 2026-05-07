import { BrowserWindow, app } from "electron";
import { fileURLToPath } from "url";
import path from "path";
//#region electron/main.js
var __dirname = path.dirname(fileURLToPath(import.meta.url));
function createWindow() {
	const win = new BrowserWindow({
		width: 1e3,
		height: 700,
		webPreferences: {
			preload: path.join(__dirname, "preload.js"),
			contextIsolation: true
		}
	});
	if (process.env.VITE_DEV_SERVER_URL) win.loadURL(process.env.VITE_DEV_SERVER_URL);
	else win.loadFile(path.join(__dirname, "../dist/index.html"));
}
app.whenReady().then(createWindow);
//#endregion
