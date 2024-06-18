const runPythonScript = require('../pythonShell');

module.exports = function (RED) {
  function CHSHGameQuantumNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const option = {
          "x": msg.payload.x, "y": msg.payload.y
        }
        runPythonScript(__dirname, 'test.py', option, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      });

      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("CHSH-game-quantum", CHSHGameQuantumNode);
}