const component=require('../../component.js');
module.exports = function(RED) {
  function StartNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
        
    node.on('input', function(msg) {
      // Always set the payload to an empty JSON object
      const root=new component.Component("root",{});
      msg.payload = {
        "structure": [root],
        "currentNode": root,
        "parentofCurrentNode": null,
        "no_of_components":0
      };
      node.send(msg);
    });

    // If you want to allow manual injection like the standard inject node
    if (config.repeat && config.repeat !== "") {
      var interval = setInterval(function() {
        node.emit("input", {});
      }, config.repeat * 1000);

      node.on('close', function() {
        clearInterval(interval);
      });
    }

    // Allow manual injection
    node.on('call:inject', function(msg) {
      node.emit("input", msg || {});
    });
  }
    
  RED.nodes.registerType("Start", StartNode);
}