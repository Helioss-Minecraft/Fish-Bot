const Command = require('../../Structures/Command');
const { MessageEmbed } = require('discord.js');
const moment = require('moment');
const Pterodactyl = require('pterodactyl.js');

module.exports = class extends Command {
  constructor(...args) {
		super(...args, {
			description: 'Fetches server ids',
			category: 'Pterodactyl'
		});
	}

  async run(message) {

    const pteroClient = new Pterodactyl.Builder()
    .setURL('https://panel.helioss.co/')
    .setAPIKey('gSvWMghKThhENkvflF0BWiZZzI6UOPKkykO9hYwOTYK1GkQI')
    .asUser();

    pteroClient.getClientServers()
    .then(async servers => {
      message.channel.send(servers[0].toJSON())

      //console.log(server.toJSON());
    }).catch(error => console.log(error));
  }
}
