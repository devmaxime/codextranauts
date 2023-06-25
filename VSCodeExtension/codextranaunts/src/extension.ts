import * as vscode from "vscode";
const axios = require("axios");
const fs = require("fs");

export function activate(context: vscode.ExtensionContext) {
  const workspaceFolders = vscode.workspace.workspaceFolders;
  let username: string;
  let repository: string;

  if (workspaceFolders) {
    const workspaceFolder = workspaceFolders[0];

    const packageJsonPath =
      workspaceFolder.uri.fsPath + "/codextranauts-next/package.json";
    fs.readFile(
      packageJsonPath,
      "utf8",
      (err: NodeJS.ErrnoException | null, data: string) => {
        if (err) {
          console.log(err);
          vscode.window.showErrorMessage("Failed to read package.json file.");
          return;
        }

        try {
          const packageJson = JSON.parse(data);
          const properties = packageJson.contributes.configuration.properties;
          username = properties["codextranaunts.githubUsername"].default;
          repository = properties["codextranaunts.repository"].default;
        } catch (error) {
          vscode.window.showErrorMessage("Failed to parse package.json data.");
        }
      }
    );
  } else {
    vscode.window.showErrorMessage("No workspace folder found.");
  }

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

      const response = await axios.post(
        "http://localhost:3000/api/LocalChanges",
        {
          username,
          repository,
          diff: customDiffWithUntrackedChanges.replace(/\0/g, ""),
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      const result = response.data;
      console.log(result);
    })
  );
}

export function deactivate() {}
module.exports = {
  activate,
};
