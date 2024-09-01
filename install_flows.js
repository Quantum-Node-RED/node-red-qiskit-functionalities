const fs = require("fs");
const path = require("path");

// Check if we're in the correct package context
const currentPackage = path.basename(process.cwd());
if (currentPackage !== "node-red-qiskit-functionalities") {
  console.log(
    "Skipping flow installation: Not in the node-red-qiskit-functionalities context."
  );
  process.exit(0); // Exit without error
}

// Determine the Node-RED user directory (usually ~/.node-red)
const nodeRedDir = path.join(
  process.env.HOME || process.env.USERPROFILE,
  ".node-red"
);
const libFlowsDir = path.join(
  nodeRedDir,
  "lib",
  "flows",
  "node-red-qiskit-functionalities"
); // Define the library flows directory with top-level node-red-qiskit-functionalities folder

// Define the paths to your flow directories
const flowDirs = [
  path.join(__dirname, "interactive-nodes/flows"),
  path.join(__dirname, "Learning/flows"),
];

// Ensure the library flows directory exists
if (!fs.existsSync(libFlowsDir)) {
  fs.mkdirSync(libFlowsDir, { recursive: true });
}

// Function to recursively find, replicate structure, and copy flow files
const copyFlowFilesRecursively = (srcDir, destDir) => {
  console.log(`Checking directory: ${srcDir}`);
  if (fs.existsSync(srcDir)) {
    fs.readdirSync(srcDir).forEach((file) => {
      const srcPath = path.join(srcDir, file);
      const destPath = path.join(destDir, file);

      // Check if it's a directory or file
      if (fs.lstatSync(srcPath).isDirectory()) {
        // Create the corresponding directory in the destination if it doesn't exist
        if (!fs.existsSync(destPath)) {
          fs.mkdirSync(destPath, { recursive: true }); // Create all intermediate directories
          console.log(`Created directory: ${destPath}`);
        }

        // Recursively copy files in the subdirectory
        copyFlowFilesRecursively(srcPath, destPath);
      } else if (
        fs.lstatSync(srcPath).isFile() &&
        path.extname(srcPath) === ".json"
      ) {
        // Only copy files with .json extension
        fs.copyFileSync(srcPath, destPath);
        console.log(`Installed ${file} from ${srcDir} to ${destPath}`);
      } else {
        console.log(`Skipping non-JSON file: ${srcPath}`);
      }
    });
  } else {
    console.warn(`Source directory ${srcDir} does not exist, skipping.`);
  }
};

// Copy flows from each directory recursively, preserving structure
flowDirs.forEach((flowDir) => {
  const relativePath = path.relative(__dirname, flowDir);
  const targetDir = path.join(libFlowsDir, relativePath); // Copying into ~/.node-red/lib/flows/node-red-qiskit-functionalities

  // Start copying files recursively, preserving the structure
  copyFlowFilesRecursively(flowDir, targetDir);
});

console.log("All flows have been installed.");
