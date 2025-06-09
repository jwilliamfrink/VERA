const { gql } = require('apollo-server-express');

module.exports = gql`
  type Entry {
    id: ID!
    code: String!
    title: String!
    summary: String!
    tags: [String!]!
    content: String!
  }

  type Query {
    entries: [Entry!]!
    entry(code: String!): Entry
  }

  type Mutation {
    createEntry(code: String!, title: String!, summary: String!, tags: [String!]!, content: String!): Entry!
    updateEntry(code: String!, title: String, summary: String, tags: [String!], content: String): Entry!
    deleteEntry(code: String!): Boolean!
  }
`;
