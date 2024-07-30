const component = require("../../component.js");
module.exports = function (RED) {
    function Quantum_Circuit_BeginNode(config) {
      RED.nodes.createNode(this, config);
      var node = this;
    
      node.on('input', function (msg) {
        msg.payload = msg.payload || {};
        const Quantum_Circuit_Begin_component = new component.Component("Quantum_Circuit_Begin",{});
        component.addComponent(msg,Quantum_Circuit_Begin_component)
        node.send(msg);
      });
    }
    RED.nodes.registerType("Quantum_Circuit_Begin", Quantum_Circuit_BeginNode);
  }
  