const { PythonShell } = require('python-shell')

const runPythonScript = (dirPath, filename, args, callback) => {
  let options = {
    mode: 'json',
    pythonOptions: ['-u'],
    // pythonPath: 'path/to/python',
    scriptPath: dirPath,
    args: JSON.stringify(args)
  };

  let result;
  let shell = new PythonShell(filename, options);
  shell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    result = message;
  });
  shell.end((err, code, signal) => {
    if (err) {
      callback(err, null);
    } else {
      callback(null, { result });
    }
  });
};

module.exports = runPythonScript;