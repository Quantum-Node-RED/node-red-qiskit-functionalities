var helper = require("node-red-node-test-helper");
var RX_gateNode = require("../interactive-nodes/Gates/RX-gate/RX-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('RX-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "RX_gate", name: "RX_gate" }];
    helper.load(RX_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "RX_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});