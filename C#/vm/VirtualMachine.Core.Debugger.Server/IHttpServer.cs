using System;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace VirtualMachine.Core.Debugger.Server
{
    public interface IHttpServer
    {
        void AddHandler(string path, HttpMethod method, Action handler);
        void AddHandler(string path, HttpMethod method, Action<JToken> handler);
        void AddHandler(string path, HttpMethod method, Func<JToken> handler);
        void AddHandler(string path, HttpMethod method, Func<JToken, JToken> handler);
        void AddHandler(string path, HttpMethod method, Func<Result<JToken>> handler);
        void AddHandler(string path, HttpMethod method, Func<JToken, Result<JToken>> handler);
        void AddHandler(string path, HttpMethod method, Func<Task<Result<JToken>>> handler);
        void AddHandler(string path, HttpMethod method, Func<JToken, Task<Result<JToken>>> handler);
        void Start();
    }
}