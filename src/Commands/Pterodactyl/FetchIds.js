const Command = require('../../Structures/Command');
const { MessageEmbed } = require('discord.js');
const moment = require('moment');
const Pterodactyl = require('pterodactyl.js');
require('dotenv').config()

this.ids = [];

module.exports = class extends Command {
  constructor(...args) {
		super(...args, {
			description: 'Fetches server ids',
			category: 'Pterodactyl'
		});
	}

  async run(message) {

    var request = require('request');
    var options = {
      'method': 'GET',
      'url': 'https://panel.helioss.co/api/application/servers',
      'headers': {
        // 'Authorization': 'Bearer ' + process.env.API_KEY,
        'Authorization': 'Bearer zXw425lT6GC0XQ4dnt6QvqRJMJIGtulHI7r6OEWMq6NmMV3y',
        'Content-Type': 'application/json',
        'Accept': 'Application/vnd.pterodactyl.v1+json'
      }
    };

    request(options, function (error, response) {
      if (error) throw new Error(error);
      //console.log(response.body);
      // console.log(typeof(response))
      var data = JSON.parse(response.body)
      for (var i=0;i<data.length;i++) {
        message.channel.send(data[i]["data"]["attributes"]["name"])
        this.ids.push({
         key:   data[i]["data"]["attributes"]["name"],
         value: data[i]["data"]["attributes"]["uuid"]
        });
      }
    });
    message.channel.send("test")
    //message.channel.send("Updated ids! First id: " + this.ids["OmniEU"]);
  }
}
