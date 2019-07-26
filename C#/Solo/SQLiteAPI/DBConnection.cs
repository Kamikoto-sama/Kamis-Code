using System.Data;
using System.Data.SQLite;
using System.IO;

namespace SQLiteAPI
{
    public class DBConnection
    {
        private readonly SQLiteConnection _connection;

        public DBConnection(string databaseName)
        {
            if (!File.Exists(databaseName))
                SQLiteConnection.CreateFile(databaseName);
            _connection = new SQLiteConnection($"DataSource={databaseName}");
            _connection.Open();
        }

        public DataTable Execute(string query)
        {
            if (query.Contains("SELECT"))
            {
                var result = new DataTable();
                new SQLiteDataAdapter(query, _connection).Fill(result);
                return result;
            }
            new SQLiteCommand(query, _connection).ExecuteNonQuery();
            return null;
        }
    }
}