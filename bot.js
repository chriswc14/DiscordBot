var config = require('./Config/config.js');
// config = config[bot];
var Discord = require('discord.js');
var client = new Discord.Client();
var bot = process.env.npm_config_bot;
// var PythonShell = require('python-shell');
// var pyshell = require('./PyShell/pyshell.js');
var fs = require('fs');

const {
    spawn
} = require('child_process');
const py = spawn('py', ['-u', './Python/mockNetwork.py']);

py.stdout.on('data', (data) => {
    console.log(data.toString('utf8'));
});

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
            console.log("Sending a message to pyshell");
            py.stdin.write(message.content + "\r\n");
            py.stdout.on('data', (data) => {
                message.reply(data.toString('utf8'));
            });
            // setTimeout(function() {
            //     fs.readFile('./netout.txt', 'utf8', function (err, contents) {
            //         message.reply(contents);
            //     });
            // }, 10000);
        }
    }
});

function saveBlock() {

}

function sendMessage() {

}

client.login(config[bot].key);