const Command = require('../../Structures/Command');
const { MessageEmbed } = require('discord.js');
const moment = require('moment');
const { exec } = require("child_process");
// const Pterodactyl = require('pterodactyl.js');

module.exports = class extends Command {
  constructor(...args) {
		super(...args, {
			description: 'Resets user to spawn (specified in level.dat)',
			category: 'Pterodactyl',
      usage: '[node] [server] [player] '
		});
	}

  async run(message, [node, server, player]) {

    // function containsObject(obj, list) {
    //   var i;
    //   for (i = 0; i < list.length; i++) {
    //       if (list[i] === obj) {
    //           return true;
    //       }
    //   }
    //
    //   return false;
    // }

    if (!message.member.roles.cache.find(role => role.name === 'Staff')) { message.channel.send("You are not authorized to to this!"); return; }
    message.channel.send("Resetting player " + player + " to spawn...")
    exec("python3 ../resetSpawn.py " + node + " " + server + " " + player, (error, stdout, stderr) => {
      if (error) {
          console.log(`error: ${error.message}`);
          return;
      }
      if (stderr) {
          console.log(`stderr: ${stderr}`);
          return;
      }
      console.log(stdout)
    });
    message.channel.send("Done!")
  }
};
