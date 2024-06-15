module.exports = function(RED) {
  function CHSHGameClassicNode(config) {
      RED.nodes.createNode(this,config);
      var node = this;
      node.on('input', function(msg) {
        let x = msg.payload.x
        let y = msg.payload.y
          
        let a = 1; // Alice's answer
        let b = 1;
       

        if(x == 0 || y == 0){
          msg.payload.result = "win"
        }else{
          msg.payload.result = "lose"
        }
        msg.payload.a = a;
        msg.payload.b = b;
        node.send(msg);
      });
  }
  RED.nodes.registerType("CHSH-game-classic",CHSHGameClassicNode);
}