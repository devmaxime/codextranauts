// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand(
    "codextranaunts.showGitChanges",
    async function () {
      // The command has been defined in the package.json file
      // Now we execute the command to show Git changes

      const vscodeGit = vscode.extensions.getExtension("vscode.git");
      const gitExtension = vscodeGit && vscodeGit.exports;
      console.log(await gitExtension.getAPI(1).repositories[0].diff(true));
      console.log(
        await gitExtension.getAPI(1).repositories[0].diff(),
        " this is diff"
      );
    }
  );

  context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
