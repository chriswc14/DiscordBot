var PythonShell = require('python-shell');
var config = require('c:\\Users\\Chris\\Desktop\\Codes\\JavaScript\\DiscordBot\\Config\\config.js');
var config2 = require('./Config/' + process.env.npm_config_bot + '.js');
var Discord = require('discord.js');
var client = new Discord.Client();
var bot = process.env.npm_config_bot;

client.on('ready', () => {
    console.log('I am ready!');
});


client.on('message', message => {
    var mentioned = false;

    if (message.author.username === bot) return;
    if (message.isMentioned(config[bot].userId)) mentioned = true;
    if (!message.content.includes(bot) && !mentioned) return;

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

client.login(config[bot].key);