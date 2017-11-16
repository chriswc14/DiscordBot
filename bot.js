var config = require('./Config/config.js');
// config = config[bot];
var Discord = require('discord.js');
var client = new Discord.Client();
var bot = process.env.npm_config_bot;
// var PythonShell = require('python-shell');
// var pyshell = require('./PyShell/pyshell.js');
var fs = require('fs');
var waitForMessage = 0;
var set = false;

// Setting up the network
const { spawn } = require('child_process');
const py = spawn('py', ['-u', './Python/mockNetwork.py']);

// Prints out python prints to console
py.stdout.on('data', (data) => {
    console.log(data.toString('utf8'));
});

// Defaults a bot if none is passed in.
if (bot == undefined) bot = 'SayTon';

// Let's User Know that Bot is ready.
client.on('ready', () => {
    console.log(bot + ' will be ready for chatting when you see NETWORK STARTUP COMPLETE!');
});

// Handles bot retrieving messages.
client.on('message', message => {
    console.log("Message Retrieved: " + message.content);
    var mentioned = false;

    // Ignore if bot is self
    if (message.author.username === bot) return;
    if (message.isMentioned(config[bot].userId)) mentioned = true;
    // Return if he should be metnioned but wasn't
    if (!message.content.includes(bot) && !mentioned && config[bot].replyToMentionOnly) return;

    if (config[bot].replyToAllMessages) {
        if (message.content.includes('Hey')) {
            message.reply('How\'s it going?');
        } else {
            console.log("Sending a message to network");
            py.stdin.write(message.content + "\r\n");

            if (!set) {
                py.stdout.on('data', (data) => {
                    set = true;
                    // Don't forget to log the message!
                    message.channel.send(data.toString('utf8'));
                    // message.reply();
                });
            }
        }
    } else {

    }
});

function saveBlock() {

}
client.login(config[bot].key);