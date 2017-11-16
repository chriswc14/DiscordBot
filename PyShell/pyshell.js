var PythonShell = require('python-shell');
var pyshell = new PythonShell('./Python/mockNetwork.py', {
    mode: 'text'
});

exports.sendMessage = function (message, callback) {
    console.log('Sending message');
    // var pyshell = new PythonShell('./Python/mockNetwork.py', {
    //     mode: 'text'
    // });

    pyshell.send('runNetwork ' + message);

    pyshell.on('message', function (message) {
        output = message;
    });

    pyshell.end(function (err) {
        if (err) return console.log(err);
        console.log('I have successfully retrived output');
        callback(output);
    });
}