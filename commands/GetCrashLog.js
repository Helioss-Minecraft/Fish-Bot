const { exec } = require("child_process");
var fs = require('fs');
// const Pterodactyl = require('pterodactyl.js');

exports.help = {
			name: "getlog",
			description: 'Gets latest crash log for provided server and node.',
			category: 'Pterodactyl',
      usage: '[node] [server]'
}

exports.run = (client, message, args, level) => {

  node = args[0]
  server = args[1]

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
  //const fileUrl = '../whereisthefile.txt' // provide file location
  var thefile = ''

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

exports.conf = {
  enabled: true,
  guildOnly: false,
  permLevel: "Moderator"
};
