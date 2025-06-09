const mongoose = require('mongoose');

const EntrySchema = new mongoose.Schema({
  code: { type: String, required: true, unique: true },
  title: String,
  summary: String,
  tags: [String],
  content: String,
});

module.exports = mongoose.model('Entry', EntrySchema);
