var helper = require("node-red-node-test-helper");
var CZ_gateNode = require("../interactive-nodes/Gates/CZ-gate/CZ-gate");
const constants = require('../interactive-nodes/constants.js');

helper.init(require.resolve('node-red'));
describe('CZ-gate Node', function () {

  beforeEach(function (done) {
    helper.startServer(done);
  });

  afterEach(function (done) {
    helper.unload();
    helper.stopServer(done);
  });

  it('should be loaded', function (done) {
    var flow = [{ id: "0", type: "CZ_gate", name: "CZ_gate" }];
    helper.load(CZ_gateNode, flow, function () {
      var n0 = helper.getNode("0");
      try {
        n0.should.have.property('name', "CZ_gate");
        done();
      } catch (err) {
        done(err);
      }
    });
  });
});