var config = require('./Config/config.js');
// config = config[bot];
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
    console.log(config);
    if (!message.content.includes(bot) && !mentioned && config[bot].replyToMentionOnly) return;

    console.log('Should speak');
    if (config[bot].replyToAllMentions == false) {
        if (message.content.includes('Hey')) {
            message.reply('How\'s it going?');
        } else {

        }
    } else {

    }
});

function saveBlock() {

}

function sendMessage() {

}

client.login(config[bot].key);