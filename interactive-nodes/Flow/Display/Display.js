const fs = require('fs');
const path = require('path');
const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function DisplayNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", async function (msg) {
      const generated_result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "../../code_generator_v3.py",
          msg.payload,
          (err, results) => {
            if (err) throw err;
            return resolve(results);
          }
        );
      });
      console.log(generated_result);

      const code_part = generated_result.result.code;

      fs.writeFileSync(path.join(__dirname, '../../generated_code.py'), code_part);

      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "../../generated_code.py",
          {},
          (err, results) => {
            if (err) throw err;
            return resolve(results);
          }
        );
      });
      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }

  RED.nodes.registerType("Display", DisplayNode);
};
