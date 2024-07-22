const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {

  const fs = require('fs');
  const path = require('path');

  function VisualizeCustomBackendNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const nodeDir = __dirname;
      const fullPath = path.join(nodeDir, 'Visualize_custom_backend.png');


      fs.readFile(fullPath, (err, data) => {
        if (err) {
          node.error("Error reading image file", err);
          return;
        }

        
        if (!msg.payload.result) {
          const result = {
            result_image: ""
          };
          msg.payload = {
            result: result
          };
        }

        const base64Image = data.toString('base64');
        msg.payload.result.result_image = base64Image;
        node.send(msg);

      });
    });
  }
  RED.nodes.registerType("visualize-custom-backend", VisualizeCustomBackendNode);
}

