const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {

  const fs = require('fs');
  const path = require('path');
  function GenerateDAGDiagramNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {

      const nodeDir = __dirname;
      const fullPath = path.join(nodeDir, 'Generate_DAG_diagram.png');


      fs.readFile(fullPath, (err, data) => {
        if (err) {
          node.error("Error reading image file", err);
          return;
        }

        const base64Image = data.toString('base64');
        msg.payload.result.result_image = base64Image;
        node.send(msg);

      });

      // const newMsg = {
      //   payload: result
      // };


      // node.send(newMsg);

    });
  }
  RED.nodes.registerType("generate-dag-for-circuit", GenerateDAGDiagramNode);
}

