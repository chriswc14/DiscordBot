var PythonShell = require('python-shell');
var pyshell = new PythonShell('./Python/mockNetwork.py', {
    mode: 'text'
});

console.log("Initializing Pyshell");
setStdout();

var output = '';
function setStdout(callback) {
    console.log("Setting stdout function for pyshell");
};

exports.sendMessage = function (message, callback) {
    console.log("Sending message ");
    // pyshell.stdout.on('data', function (data) {
    //     console.log("Retrieved a response: " + data);
    //     output += data;
    // });
    pyshell.stdout.on('data', function (data) {
        console.log("Retrieved a response: " + data);
        output = data;
        // callback(data);
    });
    pyshell.send('runNetwork ' + message).end(function (err) {
        if (err) return console.log(err);
        console.log("I have successfully retrived output");
        callback(output);
    });
}