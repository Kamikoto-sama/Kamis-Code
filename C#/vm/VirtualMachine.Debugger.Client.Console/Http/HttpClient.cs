using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using VirtualMachine.Core.Debugger;
using VirtualMachine.Core.Debugger.Client;

namespace VirtualMachine.Debugger.Client.Console.Http
{
    public class HttpClient : IHttpClient
    {
        private readonly string host;
        private readonly ushort port;

        public HttpClient(string host, ushort port)
        {
            this.host = host;
            this.port = port;
        }
        
        public async Task<Result<JToken>> PostAsync(string path, JToken content)
        {
            var stringContent = new StringContent(content.ToString(Formatting.Indented), Encoding.UTF8);
            var response = await client.PostAsync(GetUri(path), stringContent).ConfigureAwait(false);
            return JsonConvert.DeserializeObject<Result<JToken>>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));
        }

        public async Task<Result<JToken>> GetAsync(string path)
        {
            var response = await client.GetAsync(GetUri(path)).ConfigureAwait(false);
            return JsonConvert.DeserializeObject<Result<JToken>>(await response.Content.ReadAsStringAsync().ConfigureAwait(false));
        }
        
        private Uri GetUri(string path) => new Uri($"http://{host}:{port}/{path}");
        
        private readonly System.Net.Http.HttpClient client = new System.Net.Http.HttpClient();
    }
}