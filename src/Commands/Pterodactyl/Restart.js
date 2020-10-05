const Command = require('../../Structures/Command');
const { MessageEmbed } = require('discord.js');
// const moment = require('moment');
const node = require('nodeactyl')
const Client = node.Client;
const path = require('path')
// const envPath = path.resolve(__dirname, '.env')
require('dotenv').config();
//const sql = require("sqlite");
const sqlite3 = require('sqlite3').verbose();
// const dbPath = path.resolve(__dirname, 'ids.db')
let db = new sqlite3.Database('./ids.db', sqlite3.OPEN_READWRITE);

module.exports = class extends Command {
  constructor(...args) {
		super(...args, {
			description: 'Restarts a server...',
			category: 'Pterodactyl'
		});
	}

  async run(message, [server]) {
    message.channel.send(server)
    db.get(`SELECT * FROM ids WHERE name = "${server}"`, function(err, row) {
      if (!row) {
        return message.channel.send("Invalid server!")
      }

      Client.login("https://panel.helioss.co", process.env.TEST_API_KEY, (logged_in, msg) => {
        if(logged_in === false){
          return message.channel.send("Token invalid! Message: " + msg)
        }
      });

      Client.restartServer(row.id).then((response) => {
                const embed = new Discord.MessageEmbed()
                    .setTitle(response)
                    .setColor(settings.embed.color.default)
                    .setFooter(settings.embed.footer);
                message.channel.send(embed);
      }).catch((error) => {
                message.channel.send(error)
      });

    });

  }
}
