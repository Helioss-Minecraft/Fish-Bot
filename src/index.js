const DepressotronClient = require('./Structures/DepressotronClient');
const config = require('../config.json');

const client = new DepressotronClient(config);
client.start();
