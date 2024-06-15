module.exports = function(RED) {
    function CHSHClassicNode(config) {
        RED.nodes.createNode(this,config);
        var node = this;
        node.on('input', function(msg) {
            let x = msg.x
            let y = msg.y

            let a = 1
            let b = 1
            if (x == 0 || y == 0) {
                msg.result = "win"
            }else{
                msg.result = "lose"
            }
            msg.a = a
            msg.b = b
            node.send(msg);
        });
    }
    RED.nodes.registerType("CHSH-game-classic",CHSHClassicNode);













}

