const Entry = require('./models/Entry');

module.exports = {
  Query: {
    entries: async () => Entry.find(),
    entry: async (_, { code }) => Entry.findOne({ code }),
  },
  Mutation: {
    createEntry: async (_, args) => Entry.create(args),
    updateEntry: async (_, { code, ...updates }) =>
      Entry.findOneAndUpdate({ code }, updates, { new: true }),
    deleteEntry: async (_, { code }) =>
      (await Entry.deleteOne({ code })).deletedCount === 1,
  },
};
