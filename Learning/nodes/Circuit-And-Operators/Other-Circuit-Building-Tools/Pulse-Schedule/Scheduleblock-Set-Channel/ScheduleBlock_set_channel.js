const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function ScheduleBlockSetChannelNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on('input',  async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have  learned this node." });

      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "ScheduleBlock_set_channel.py", arg = null, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      
      });

      const newMsg = {
        payload: result
      }


      node.send(newMsg);
    });

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType("scheduleblock-set-channel", ScheduleBlockSetChannelNode);
}

