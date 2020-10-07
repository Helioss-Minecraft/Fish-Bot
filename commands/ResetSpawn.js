const { exec } = require("child_process");
// const Pterodactyl = require('pterodactyl.js');


exports.help = {
			name: "resetspawn",
			description: 'Resets user to spawn (specified in level.dat)',
			category: 'Pterodactyl',
      usage: '[node] [server] [player] '
}


exports.run = async (client, message, args, level) => {
  node = args[0]
  server = args[1]
  player = args[2]

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

    // if (!message.member.roles.cache.find(role => role.name === 'Staff')) { message.channel.send("You are not authorized to to this!"); return; }
    message.channel.send("Resetting player " + player + " to spawn...")
    exec("python3 resetSpawn.py " + node + " " + server + " " + player, (error, stdout, stderr) => {
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

  exports.conf = {
    enabled: true,
    guildOnly: true,
    aliases: [],
    permLevel: "Moderator"
  };
