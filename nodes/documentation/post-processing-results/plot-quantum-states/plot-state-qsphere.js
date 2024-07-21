const runPythonScript = require("../../../pythonShell");

module.exports = function(RED) {
    function PlotStateQsphereNode(config) {
        RED.nodes.createNode(this,config);
        var node = this;
        node.on('input', async function(msg) {
            const result = await new Promise((resolve, reject) => {
                const option = {
                
                };
                runPythonScript(__dirname, "plot-state-qsphere.py", option, (err, results) => {
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
    RED.nodes.registerType("plot-state-qsphere", PlotStateQsphereNode);
}