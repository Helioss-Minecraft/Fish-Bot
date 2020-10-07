const { exec } = require("child_process");
// const Pterodactyl = require('pterodactyl.js');

exports.help = {
		name: "resetcoords",
		description: 'Resets user to specified coords...',
		category: 'Pterodactyl',
    usage: 'resetcoords [node] [server] [player] [xCoord] [yCoord] [zCoord] [dim]'
	}

exports.run =  async (client, message, args, level) => {
  node = args[0]
  server = args[1]
  player = args[2]
  xCoord = args[3]
  yCoord = args[4]
  zCoord = args[5]
  dim = args[6]


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
    message.channel.send("Resetting player " + player + " to coords: " + xCoord + ", " + yCoord + ", " + zCoord + " " + "in dimension " + dim + "...")
    exec("python3 resetpos.py " + node + " " + server + " " + player + " " + xCoord + " " + yCoord + " " + zCoord + " " + dim, (error, stdout, stderr) => {
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
