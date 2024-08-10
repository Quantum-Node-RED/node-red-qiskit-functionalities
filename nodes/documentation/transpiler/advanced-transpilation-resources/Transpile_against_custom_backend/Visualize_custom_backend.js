const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {

  const fs = require('fs');
  const path = require('path');

  function VisualizeCustomBackendNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;
    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on('input',  async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have  learned this node." });

      const nodeDir = __dirname;
      const fullPath = path.join(nodeDir, 'Visualize_custom_backend.png');


      fs.readFile(fullPath, (err, data) => {
        if (err) {
          node.error("Error reading image file", err);
          return;
        }

        
        msg.payload = {result: {result_image: ''}};

        const base64Image = data.toString('base64');
        msg.payload.result.result_image = base64Image;
        node.send(msg);

      });
    });

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType("visualize-custom-backend", VisualizeCustomBackendNode);
}

