var helper = require("node-red-node-test-helper");
var H_gateNode = require("../interactive-nodes/Gates/H-gate/H-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('H-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "H_gate", name: "H_gate" }];
    helper.load(H_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "H_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});