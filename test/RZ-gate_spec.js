var helper = require("node-red-node-test-helper");
var RZ_gateNode = require("../interactive-nodes/Gates/RZ-gate/RZ-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('RZ-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "RZ_gate", name: "RZ_gate" }];
    helper.load(RZ_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "RZ_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});