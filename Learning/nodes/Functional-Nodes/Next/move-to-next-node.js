// const runPythonScript = require("../.././../../pythonShell");
// var recievedMsg = null;

module.exports = function (RED) {
  function MoveToNextNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;

    node.context().set("recievedMsg", null);
    
    node.on("input",  function (msg) {
      try {
        node.context().set("recievedMsg", msg);
        // console.log('Message received and processed');
      } catch (err) {
        node.error('Error processing input message:', err);
      }
    });

    node.on("close", function () {
      node.removeAllListeners("input");
      node.context().set("recievedMsg", null);
    });
  }
  RED.nodes.registerType("move-to-next-node", MoveToNextNode);
  
  RED.httpAdmin.post('/Next/:id', RED.auth.needsPermission('inject.write'), function (req, res) {
    const node = RED.nodes.getNode(req.params.id);
    if (node) {
      try {
        const recievedMsg = node.context().get("recievedMsg");
        if (recievedMsg){
          var msg = { payload: "Next" }
          node.send(msg);
          node.done();
        }else{
          node.error(RED._('Please start from the beginning'));
        }
      } catch (err) {
        res.sendStatus(500);
        // node.error(RED._('nameinject.failed', { error: err.toString() }));
      }
    } else {
      res.sendStatus(404);
    }
  });
};

