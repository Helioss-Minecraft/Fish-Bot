// The MESSAGE event runs anytime a message is received
// Note that due to the binding of client to every event, every event
// goes `client, other, args` when this function is run.

function findServer(id) {
  var botservers = {
    "740569319859290192": "ATM3R",
    //"621874860544622605": "SAOTS",
    "649006702838153219": "DDSSEU",
    "734049639765901352": "E2ENA",
    "641136331204067348": "E2EEU",
    "740374864262725684": "FTBI",
    "740883398574211083": "GTNH",
    "721460605801857084": "MCE",
    "652700521039396876": "OmniEU",
    "686962653507354689": "OmniNA",
    "713484865949139008": "PO3NA",
    "724381251745874012": "SAOTS"
  }
  return botservers[id]
}

function findNode(id) {
  var serv = findServer(id)
  var botnodes = {
    "ATM3R": "germany",
    "DDSSEU": "germany",
    "E2ENA": "canada",
    "E2EEU": "london",
    "FTBI": "germany",
    "GTNH": "germany",
    "MCE": "london",
    "OmniEU": "london",
    "OmniNA": "canada",
    "PO3NA": "canada",
    "SAOTS": "london",
  }
  return botnodes[serv]
}

function wait(ms){
  var start = new Date().getTime();
  var end = start;
  while(end < start + ms) {
    end = new Date().getTime();
  }
}

module.exports = async (client, message) => {
  // It's good practice to ignore other bots. This also makes your bot ignore itself
  // and not get into a spam loop (we call that "botception").
  if (message.author.bot) return;

  // Grab the settings for this server from Enmap.
  // If there is no guild, get default conf (DMs)
  const settings = message.settings = client.getSettings(message.guild);

  // Checks if the bot was mentioned, with no message after it, returns the prefix.
  const prefixMention = new RegExp(`^<@!?${client.user.id}>( |)$`);
  if (message.content.match(prefixMention)) {
    return message.reply(`My prefix on this guild is \`${settings.prefix}\``);
  }

  if (message.content.includes("Server Crash Detected")) {
    // message.channel.send("test detected crash :D")
    // require("downloadjs")("http://ovh.helioss.co:1111");
    const { exec } = require("child_process");

    // var url = "http://ovh.helioss.co:1111/c109582e-dc78-4a24-b256-630afca1b88c/world/level.dat"
    // message.channel.send("Downloaded level.dat from " + url)
    // exec("wget --http-user=6b9164e2052e92c2c9e049da66c423e1781a55086f9b00e3a1f9f0bc04df846f26dae0a037c74ea1d9c6f68ed0906d9807a7a97a49b37610baacd89542cda2f0 --http-password=c289ee0bf6ac91fc19b603f8ccc9459ff2ee5baf5cfc0cc2db985fa4ac87357c44aa70fc8b9a9276e6f7228b135f32d68840185111bedd31f5c4b52bf3fb0a31 " + url, (error, stdout, stderr) => {
    // 	if (error) {
    //   		console.log(`error: ${error.message}`);
    //   		return;
    // 	}
    // 	if (stderr) {
    //   		console.log(`stderr: ${stderr}`);
    //   		return;
    // 	}
    // 	console.log(`stdout: ${stdout}`);
    // });
    exec("python3 downloadlatest.py " + findNode(message.author.id) + " " + findServer(message.author.id), (error, stdout, stderr) => {
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
    const fileUrl = '../whereisthefile.txt' // provide file location
    var thefile = ''
    var fs = require('fs');

    // fs.readFile(fileUrl, 'utf8', function(err, contents) {
    // 	thefile = contents
    // });

    const testFolder = '..';
    // const fs = require('fs');

    var glob = require("glob")

    wait(3000)
    // options is optional
    glob("crash-reports/*.txt", function (er, files) {
      // files is an array of filenames.
      // If the `nonull` option is set, and nothing
      // was found, then files is ["**/*.js"]
      // er is an error object or null.
      thefile = files[0];
      console.log(thefile)
      console.log(files)
      // console.log(er)
      const attachment = new MessageAttachment('./' + thefile);
      message.client.channels.cache.get('732258457721503764').send("Server " + findServer(message.author.id) + " crashed, here is the crash report!", attachment);
      // fs.unlinkSync("./" + thefile)
    })
  }

  // Also good practice to ignore any message that does not start with our prefix,
  // which is set in the configuration file.
  if (message.content.indexOf(settings.prefix) !== 0) return;

  // Here we separate our "command" name, and our "arguments" for the command.
  // e.g. if we have the message "+say Is this the real life?" , we'll get the following:
  // command = say
  // args = ["Is", "this", "the", "real", "life?"]
  const args = message.content.slice(settings.prefix.length).trim().split(/ +/g);
  const command = args.shift().toLowerCase();

  // If the member on a guild is invisible or not cached, fetch them.
  if (message.guild && !message.member) await message.guild.members.fetch(message.author);

  // Get the user or member's permission level from the elevation
  const level = client.permlevel(message);

  // Check whether the command, or alias, exist in the collections defined
  // in app.js.
  const cmd = client.commands.get(command) || client.commands.get(client.aliases.get(command));
  // using this const varName = thing OR otherThing; is a pretty efficient
  // and clean way to grab one of 2 values!
  if (!cmd) return;

  // Some commands may not be useable in DMs. This check prevents those commands from running
  // and return a friendly error message.
  if (cmd && !message.guild && cmd.conf.guildOnly)
    return message.channel.send("This command is unavailable via private message. Please run this command in a guild.");

  if (level < client.levelCache[cmd.conf.permLevel]) {
    if (settings.systemNotice === "true") {
      return message.channel.send(`You do not have permission to use this command.
  Your permission level is ${level} (${client.config.permLevels.find(l => l.level === level).name})
  This command requires level ${client.levelCache[cmd.conf.permLevel]} (${cmd.conf.permLevel})`);
    } else {
      return;
    }
  }

  // To simplify message arguments, the author's level is now put on level (not member so it is supported in DMs)
  // The "level" command module argument will be deprecated in the future.
  message.author.permLevel = level;

  message.flags = [];
  while (args[0] && args[0][0] === "-") {
    message.flags.push(args.shift().slice(1));
  }
  // If the command exists, **AND** the user has permission, run it.
  client.logger.cmd(`[CMD] ${client.config.permLevels.find(l => l.level === level).name} ${message.author.username} (${message.author.id}) ran command ${cmd.help.name}`);
  cmd.run(client, message, args, level);
};
