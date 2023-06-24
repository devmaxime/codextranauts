// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use vscode.workspace.onDidSaveTextDocument event to trigger your function when any file in the workspace is saved.
  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(async () => {
      const vscodeGit = vscode.extensions.getExtension("vscode.git");
      const gitExtension = vscodeGit && vscodeGit.exports;
      const repo = await gitExtension.getAPI(1).repositories[0];

      const workingTreeChanges = repo.state.workingTreeChanges;
      let customDiffWithUntrackedChanges = "";

      const untrackedFiles = workingTreeChanges.filter(
        (change: { status: number }) => {
          if (change.status === 7) {
            return true;
          }
        }
      );

      for (const file of untrackedFiles) {
        vscode.workspace.fs
          .readFile(file.a.resourceUri)
          .then((fileData: Uint8Array) => {
            customDiffWithUntrackedChanges += `${
              file.a.resourceUri
            }\n+ ${Buffer.from(fileData).toString()}\n`;
          });
      }

      const trackedFilesDiff = await repo.diff();
      customDiffWithUntrackedChanges += trackedFilesDiff;
      console.log(customDiffWithUntrackedChanges);
    })
  );
}

// This method is called when your extension is deactivated
export function deactivate() {}
