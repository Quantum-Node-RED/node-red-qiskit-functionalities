module.exports = function (RED) {
  function CHSHGameClassicNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on('input', function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have  learned this node." });
      msg.payload.x = msg.payload.x || 0;
      msg.payload.y = msg.payload.y || 0;


      let x = msg.payload.x
      let y = msg.payload.y

      let a = 1; // Alice's answer
      let b = 1;


      if (x == 0 || y == 0) {
        msg.payload.result = { a: 1, b: 1, result: "win" }
      } else {
        msg.payload.result = { a: 1, b: 1, result: "lose" }
      }
      node.send(msg);
    });
  }
  RED.nodes.registerType("CHSH-game-classic", CHSHGameClassicNode);
}