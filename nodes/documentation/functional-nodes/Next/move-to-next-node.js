// const runPythonScript = require("../.././../../pythonShell");
var recievedMsg = null;

module.exports = function (RED) {
  function MoveToNextNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    
    node.on("input", async function (msg) {
      recievedMsg = msg;
    });

    node.on("close", function () {
      recievedMsg = null;
    });
  }
  RED.nodes.registerType("move-to-next-node", MoveToNextNode);
  
  RED.httpAdmin.post('/Next/:id', RED.auth.needsPermission('inject.write'), function (req, res) {
    const node = RED.nodes.getNode(req.params.id)
    if (node) {
      try {
        if (recievedMsg){
          var msg = { payload: "Next" }
          node.send(msg)
        }else{
          node.error(RED._('Please start from the beginning'))
        }
      } catch (err) {
        res.sendStatus(500)
        node.error(RED._('nameinject.failed', { error: err.toString() }))
      }
    } else {
      res.sendStatus(404)
    }
  });
};

