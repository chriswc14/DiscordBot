var Discord = require('discord.js');

var client = new Discord.Client();

client.on('ready', () => {
    console.log('I am ready!');
});

client.on('message', message => {
    if (message.content === 'ping') {
        message.reply('pong');
    }
});

client.login('MzcwMzU4MzMzNzk1NzI5NDI5.DMl6qA.qh1pIxKaWWj-v_LKZYHsLWaMsVI');