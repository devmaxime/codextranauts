"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
function activate(context) {
    let disposable = vscode.commands.registerCommand("codextranaunts.showGitChanges", async function () {
        // The command has been defined in the package.json file
        // Now we execute the command to show Git changes
        const vscodeGit = vscode.extensions.getExtension("vscode.git");
        const gitExtension = vscodeGit && vscodeGit.exports;
        console.log(await gitExtension.getAPI(1).repositories[0].diff(true));
        console.log(await gitExtension.getAPI(1).repositories[0].diff(), " this is diff");
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
// This method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map