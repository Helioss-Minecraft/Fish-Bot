const Event = require('../../Structures/Event');
const http = require('http');
const { MessageAttachment } = require('discord.js');
const fs = require('fs');
const axios = require('axios');

module.exports = class extends Event {




	async run(message) {

		function findServer(id) {
			var botservers = {
				"740569319859290192": "ATM3R",
				// "621874860544622605": "ATM3R",
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

		const mentionRegex = RegExp(`^<@!${this.client.user.id}>$`);
		const mentionRegexPrefix = RegExp(`^<@!${this.client.user.id}> `);

		if (!message.guild || message.author.bot) return;

		if (message.content.match(mentionRegex)) message.channel.send(`My prefix for ${message.guild.name} is \`${this.client.prefix}\`.`);

		const prefix = message.content.match(mentionRegexPrefix) ?
			message.content.match(mentionRegexPrefix)[0] : this.client.prefix;

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
			exec("python3 ../downloadlatest.py " + findNode(message.author.id) + " " + findServer(message.author.id), (error, stdout, stderr) => {
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

			wait(1000)
			// options is optional
			glob("./*.txt", function (er, files) {
  			// files is an array of filenames.
  			// If the `nonull` option is set, and nothing
  			// was found, then files is ["**/*.js"]
  			// er is an error object or null.
				thefile = files[0];
				// console.log(thefile)
				// console.log(files)
				// console.log(er)
				const attachment = new MessageAttachment('./' + thefile);
				message.client.channels.cache.get('732258457721503764').send("Server " + findServer(message.author.id) + " crashed, here is the crash report!", attachment);
				// fs.unlinkSync("./" + thefile)
			})
			// console.log(thefile)

		}


		const [cmd, ...args] = message.content.slice(prefix.length).trim().split(/ +/g);

		const command = this.client.commands.get(cmd.toLowerCase()) || this.client.commands.get(this.client.aliases.get(cmd.toLowerCase()));
		if (command) {
			command.run(message, args);
		}
	}

};
