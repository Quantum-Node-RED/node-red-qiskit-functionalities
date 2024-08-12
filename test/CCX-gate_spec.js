var helper = require("node-red-node-test-helper");
var CCX_gateNode = require("../interactive-nodes/Gates/CCX-gate/CCX-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('CCX-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "CCX_gate", name: "CCX_gate" }];
    helper.load(CCX_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "CCX_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});