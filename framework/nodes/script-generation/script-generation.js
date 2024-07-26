const runPythonScript = require("../../pythonShell");
const fs = require("fs");
const path = require("path");
const { createCanvas, loadImage } = require("canvas");

module.exports = function (RED) {
  function ScriptGenerationNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", async function (msg) {
      const data = msg.payload;

      // Ensure the payload is initialized
      if (!msg.payload) {
        msg.payload = {};
      }

      if (!data.algorithm) {
        node.error("Algorithm not found");
        return;
      }

      file = get_algorithm_file(data.algorithm);

      // Read the content of the Python file
      const filePath = path.join(__dirname, file);
      fs.readFile(filePath, "utf8", (err, fileContent) => {
        if (err) {
          node.error("Error reading the Python file: " + err.message);
          return;
        }

        // Create an image from the Python file content
        const canvasWidth = 800;
        const canvasHeight = 20 * fileContent.split("\n").length; // Estimate height based on line count
        const canvas = createCanvas(canvasWidth, canvasHeight);
        const ctx = canvas.getContext("2d");
        ctx.font = "16px Courier";
        ctx.fillStyle = "#000000";
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);
        ctx.fillStyle = "#ffffff";

        const lines = fileContent.split("\n");
        lines.forEach((line, index) => {
          ctx.fillText(line, 10, 20 * (index + 1));
        });

        const buffer = canvas.toBuffer("image/png");
        const base64Image = buffer.toString("base64");
        const imageDataUri = "data:image/png;base64," + base64Image;

        // Print the content of the Python file
        console.log("Python File Content:\n", fileContent);

        // Run the Python script
        runPythonScript(__dirname, file, data, (err, result) => {
          if (err) {
            node.error("Error running Python script: " + err.message);
            return;
          }

          // Send the result and the image of the file content in the payload
          msg.payload = result;
          msg.payload.pythonFileImage = imageDataUri;
          node.send(msg);
        });
      });
    });
  }

  function get_algorithm_file(algorithm) {
    if (algorithm === "QAOA") {
      return "../../algorithms/QAOA/QAOA_circuit.py";
    } else if (algorithm === "VQE") {
      return "../../algorithms/VQE/VQE.py";
    } else {
      throw new Error("Algorithm file not found");
    }
  }

  RED.nodes.registerType("script-generation", ScriptGenerationNode);
};
