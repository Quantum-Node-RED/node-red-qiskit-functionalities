var helper = require("node-red-node-test-helper");
var CX_gateNode = require("../interactive-nodes/Gates/CX-gate/CX-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('CX-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "CX_gate", name: "CX_gate" }];
    helper.load(CX_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "CX_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });

  // it('should produce the correct payload', function (done) {
  //   // Define the flow with CX_gateNode and a helper node
  //   var flow = [
  //     {
  //       id: "n1",
  //       type: "CX_gate",
  //       control_qubit: 1,
  //       wires: [["n2"]]
  //     },
  //     { id: "n2", type: "helper" } // Helper node to receive the output
  //   ];

  //   // Load the nodes and run the test
  //   helper.load(CX_gateNode, flow, function () {
  //     var n1 = helper.getNode("n1");
  //     var n2 = helper.getNode("n2");
  //     n1.context().flow.set(constants.CIRCUIT_NAME, "test_circuit");
  //     console.log(111);

  //     // Listen for input on the helper node
  //     n2.on("input", function (msg) {
  //       // Validate that the payload is produced correctly
  //       msg.should.have.property('payload');
  //       console.log(msg);
  //       msg.payload.should.have.property('qubit_id', 0); // Expected output qubit_id from CX_gate
  //       msg.payload.should.have.property('control_qubit', 2); // Control qubit from configuration

  //       done(); // End the test
  //     });

  //     console.log("Sending message to CX_gateNode");

  //     // Simulate receiving a message with qubit_id in the payload from the previous node
  //     n1.receive({
  //       payload: {
  //         structure: [],
  //         currentNode: {},
  //         parentofCurrentNode: {},
  //         qubit_id: 0
  //       }
  //     });
  //   });
  // });
});