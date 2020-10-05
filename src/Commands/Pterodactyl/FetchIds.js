const Command = require('../../Structures/Command');
const { MessageEmbed } = require('discord.js');
const moment = require('moment');
const node = require('nodeactyl')
const Application = node.Application;
require('dotenv').config()
//const sql = require("sqlite");
const sqlite3 = require('sqlite3').verbose();
// const path = require('path')
// const dbPath = path.resolve(__dirname, 'ids.db')
let db = new sqlite3.Database('./ids.db', sqlite3.OPEN_READWRITE);


module.exports = class extends Command {
  constructor(...args) {
		super(...args, {
			description: 'Fetches server ids',
			category: 'Pterodactyl'
		});
	}

  async run(message) {

    Application.login("https://panel.helioss.co", process.env.APPLICATION_API_KEY, (logged_in) => {
                if(logged_in === false){
                  return message.channel.send("Token invalid!")
                }


    });

    Application.getAllServers().then(servers => {
      for (var i=0;i<servers.length;i++) {
            message.channel.send(servers[i]["attributes"]["name"])
            db.run(`INSERT INTO ids (name, id) VALUES ("${servers[i]["attributes"]["name"]}", "${servers[i]["attributes"]["uuid"]}")`, function(err) {
              if (err) {
                return message.channel.send("SQLite Error: " + err)
              }
            });
           //  this.ids.push({
           //   key:   servers[i]["attributes"]["name"],
           //   value: servers[i]["attributes"]["uuid"]
           //   });
      }
    });

  //   var request = require('request');
  //   var options = {
  //     'method': 'GET',
  //     'url': 'https://panel.helioss.co/api/application/servers',
  //     'headers': {
  //       'Authorization': 'Bearer ' + process.env.API_KEY,
  //       'Content-Type': 'application/json',
  //       'Accept': 'Application/vnd.pterodactyl.v1+json'
  //     }
  //   };
  //
  //   request(options, function (error, response) {
  //     if (error) throw new Error(error);
  //     //console.log(response.body);
  //     // console.log(typeof(response))
  //     var data = JSON.parse(response.body)
  //     for (var i=0;i<data.length;i++) {
  //       message.channel.send(data[i]["data"]["attributes"]["name"])
  //       this.ids.push({
  //        key:   data[i]["data"]["attributes"]["name"],
  //        value: data[i]["data"]["attributes"]["uuid"]
  //       });
  //     }
  //   });
  //   message.channel.send("test")
  //   //message.channel.send("Updated ids! First id: " + this.ids["OmniEU"]);
  }
}
