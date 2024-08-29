var helper = require("node-red-node-test-helper");
var X_gateNode = require("../interactive-nodes/Gates/X-gate/X-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('X-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "X_gate", name: "X_gate" }];
    helper.load(X_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "X_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});