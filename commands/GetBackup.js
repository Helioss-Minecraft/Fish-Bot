const { exec } = require("child_process");
// const Pterodactyl = require('pterodactyl.js');

exports.help = {
			name: "getbackup",
			description: 'Gets a backup and shoves it into /var/www/, and tells you the link.',
			category: 'Pterodactyl',
      usage: '[uuid] [date/latest]'
}
exports.run = (client, message, args, level) => {

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
    message.channel.send("Getting backup...")
    exec("python3 getbackup " + args[0] + " " + args[1], (error, stdout, stderr) => {
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
	  permLevel: "Moderator"
	};
