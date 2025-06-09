import { useQuery, gql } from '@apollo/client';

const GET_ENTRIES = gql`
  query GetEntries {
    entries {
      code
      title
      summary
      tags
    }
  }
`;

function Home() {
  const { loading, error, data } = useQuery(GET_ENTRIES);

  if (loading) return <p className="p-6">Loading...</p>;
  if (error) return <p className="p-6 text-red-600">Error: {error.message}</p>;

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">VERA Wiki</h1>
      {data.entries.map((entry) => (
        <div key={entry.code} className="mb-4 p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">{entry.title}</h2>
          <p className="text-sm text-gray-600">{entry.code}</p>
          <p className="mt-2 text-gray-700">{entry.summary}</p>
          <div className="mt-2">
            {entry.tags.map(tag => (
              <span
                key={tag}
                className="inline-block bg-gray-200 text-gray-800 text-xs px-2 py-1 rounded mr-2"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Home;
