const runPythonScript = require("../../pythonShell");
module.exports = function (RED) {
  function EndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", async function (msg) {
      const result = await new Promise((resolve, reject) => {
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
      console.log(result);
      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }

  RED.nodes.registerType("End", EndNode);
};
