var helper = require("node-red-node-test-helper");
var I_gateNode = require("../interactive-nodes/Gates/I-gate/I-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('I-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "I_gate", name: "I_gate" }];
    helper.load(I_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "I_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});