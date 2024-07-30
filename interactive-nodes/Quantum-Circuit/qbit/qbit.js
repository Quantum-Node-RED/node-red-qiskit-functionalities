const component = require("../../component.js");
module.exports = function (RED) {
    function qbitNode(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        node.on('input', function (msg) {
            msg.payload = msg.payload || {};
            const qbit_component = new component.Component("qbit", {});
            component.addComponent(msg, qbit_component);
            node.send(msg);
        });
    }
    
    RED.nodes.registerType("qbit", qbitNode);
};
