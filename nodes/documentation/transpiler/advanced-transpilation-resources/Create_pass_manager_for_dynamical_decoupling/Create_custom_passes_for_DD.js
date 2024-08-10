const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function CreateCustomPassForDDNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on('input',  async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have  learned this node." });

      // if(!msg.token){
      //   node.error("Token is not provided. Please configure 'Get Backend Operation Names' node with a valid token.", msg);
      //   return;
      // }


      try{
        const result = await new Promise((resolve,reject) => {
          const options = {
            token: msg.token
          };

          runPythonScript(__dirname, "Create_custom_passes_for_DD.py", arg = options, (err, results) => {
            if (err) {
              reject(err); 
              return;
            }
            resolve(results);
          });
        
        });

        const newMsg = {
          payload: result,
          token: msg.token
        };


        node.send(newMsg);
      }catch(error){
        node.error(`Error running Python script: ${error.message}`, msg);
      }
    });

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType("create-custom-pass-for-dd", CreateCustomPassForDDNode);
}

