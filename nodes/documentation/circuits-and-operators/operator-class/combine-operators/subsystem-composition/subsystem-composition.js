const runPythonScript = require("../../../../../pythonShell");

module.exports = function (RED) {
  function SubsystemComposition(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;

    node.on("input", async function (msg) {
      const option = {};
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "subsystem-composition.py",
          option,
          (err, results) => {
            if (err) reject(err);
            resolve(results);
          }
        );
      });

      const newMsg = {
        payload: result,
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("Subsystem-Composition", SubsystemComposition);
};
