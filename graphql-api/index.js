import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';
import gql from 'graphql-tag';

dotenv.config();

const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017';
const client = new MongoClient(uri);
await client.connect();
const db = client.db('vera');
const ethicsCollection = db.collection('ethics_documents');

// --- GraphQL schema ---
const typeDefs = gql`
  type Source {
    url: String
    publisher: String
    retrievedDate: String
  }

  type Document {
    id: ID
    title: String
    type: String
    jurisdiction: String
    tags: [String]
    applicability: [String]
    license: String
    publisher: String
    status: String
    content: String
    universalPrinciples: [String]
    source: Source
  }

input FilterInput {
  type: String
  status: String
  publisher: String
  jurisdiction: String
  license: String
  tags: [String]
  applicability: [String]
  sourcePublisher: String # <-- an example of "dot notation" for nested fields
}

  type Query {
    filteredDocuments(filter: FilterInput): [Document]
  }
`;

// --- Resolvers ---
const resolvers = {
  Query: {
    filteredDocuments: async (_, { filter }, { db }) => {
        const query = {};
        if (!filter) {
            return await db.collection('ethics_documents').find().toArray();
        }

        Object.entries(filter).forEach(([key, value]) => {
            const mongoKeyMap = {
                sourcePublisher: 'source.publisher',
                // Add more field maps if needed
            };
            
            const mongoKey = mongoKeyMap[key] || key;
            query[mongoKey] = Array.isArray(value)
                ? { $in: value }
                : value;
        });
        
        return await db.collection('ethics_documents').find(query).toArray();
    }
  }
};

// --- Start Apollo Server ---
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  context: async () => ({ db }),
});

console.log(`🚀 Server ready at ${url}`);