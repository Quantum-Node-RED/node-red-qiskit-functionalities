var helper = require("node-red-node-test-helper");
var U_gateNode = require("../interactive-nodes/Gates/U-gate/U-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('U-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "U_gate", name: "U_gate" }];
    helper.load(U_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "U_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});