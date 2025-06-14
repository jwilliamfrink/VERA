import { useState } from 'react';
import { useQuery, gql } from '@apollo/client';

const GET_ENTRIES = gql`
  query GetEntries {
    entries {
      id
      title
      summary
      tags
    }
  }
`;

function Home() {
  const { loading, error, data } = useQuery(GET_ENTRIES);
  const [comments, setComments] = useState({});
  const handleVote = (id, type) => {
    console.log(`Voted ${type} on ${id}`);
  };
  const handleComment = (id) => {
    console.log(`Comment on ${id}:`, comments[id]);
  };

  if (loading) return <p className="p-6">Loading...</p>;
  if (error) return <p className="p-6 text-red-600">Error: {error.message}</p>;

  return (
    <div className="p-6 max-w-3xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">VERA Ethical Records Explorer</h1>
      <p className="text-gray-600">Browse and interact with ethical principles. Filter and explore without writing queries.</p>

      {data.entries.map(entry => (
        <div key={entry.id} className="p-4 bg-white rounded shadow space-y-2">
          <h2 className="text-xl font-semibold">{entry.title}</h2>
          <p className="text-gray-700">{entry.summary}</p>
          <div className="text-sm text-gray-500">Tags: {entry.tags.join(', ')}</div>

          <div className="flex space-x-2">
            <button onClick={() => handleVote(entry.id, 'up')} className="bg-green-100 text-green-700 px-2 py-1 rounded">Upvote</button>
            <button onClick={() => handleVote(entry.id, 'down')} className="bg-red-100 text-red-700 px-2 py-1 rounded">Downvote</button>
          </div>

          <div>
            <textarea
              className="w-full p-2 border rounded"
              placeholder="Leave a comment"
              value={comments[entry.id] || ''}
              onChange={e => setComments({ ...comments, [entry.id]: e.target.value })}
            />
            <button onClick={() => handleComment(entry.id)} className="mt-2 bg-blue-600 text-white px-4 py-1 rounded">Submit Comment</button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default Home;
