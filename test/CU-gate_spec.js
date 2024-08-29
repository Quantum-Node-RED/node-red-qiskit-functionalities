var helper = require("node-red-node-test-helper");
var CU_gateNode = require("../interactive-nodes/Gates/CU-gate/CU-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('CU-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "CU_gate", name: "CU_gate" }];
    helper.load(CU_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "CU_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});