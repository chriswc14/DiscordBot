var config = require('./Config/config.js');
var Discord = require('discord.js');
var client = new Discord.Client();
var bot = process.env.npm_config_bot;
// var PythonShell = require('python-shell');
var pyshell = require('./PyShell/pyshell.js');

if (bot == undefined) {
    bot = 'SayTon';
}

client.on('ready', () => {
    console.log(bot + ' is ready for chatting!');
});

client.on('message', message => {
    var mentioned = false;

    if (message.author.username === bot) return;
    if (message.isMentioned(config[bot].userId)) mentioned = true;
    console.log(message.content);
    // if (!message.content.includes(bot) && !mentioned) return;

    console.log('Should speak');
    if (message.content.includes('Hey')) {
        message.reply('How\'s it going?');
    } else if (message.content.includes(' ')) {
        console.log("Sending a message to pyshell");
        pyshell.sendMessage(message.content, function (response) {
            console.log("I am responding with: " + response);
            client.sendMessage(response);
        });
        // PythonShell.run('./Python/randomResponses.py', function (err, results) {
        //     if (err) throw err;
        //     var randomNum = Math.floor(Math.random() * 10);
        //     message.reply(results[randomNum]);
        // });

        // Pyshell test
        // var pyshell = new PythonShell('./Python/echo_text.py', {
        //     mode: 'text'
        // });
        // var output = '';
        // pyshell.stdout.on('data', function (data) {
        //     output += '' + data;
        // });
        // pyshell.send('hello').send('world').end(function (err) {
        //     if (err) {

        //         console.log("I fail");
        //         console.log(err);
        //         return err;
        //     } else {
        //         console.log("I PASSED");
        //     }
        // });
    }
});

client.login(config[bot].key);
