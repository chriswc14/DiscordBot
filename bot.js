var Discord = require('discord.js');
var PythonShell = require('python-shell');
var client = new Discord.Client();

client.on('ready', () => {
    console.log('I am ready!');
});


client.on('message', message => {
    if (message.author.username === "SayTon") return;

    if (message.content.includes('Hey')) {
        message.reply('How\'s it going?');
    } else if (message.content.includes(' ')) {
        PythonShell.run('./Python/randomResponses.py', function (err, results) {
            if (err) throw err;
            var randomNum = Math.floor(Math.random() * 10);
            message.reply(results[randomNum]);
        });
    }
});

client.login('MzcwMzY1MjQ0Mzg1NjU2ODUy.DMpwRw.B0oK1fvkQG8sOJLKVokB2wjKZ28');