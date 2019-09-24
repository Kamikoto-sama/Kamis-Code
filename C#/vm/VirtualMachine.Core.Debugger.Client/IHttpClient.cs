using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace VirtualMachine.Core.Debugger.Client
{
    public interface IHttpClient
    {
        Task<Result<JToken>> PostAsync(string path, JToken content);
        Task<Result<JToken>> GetAsync(string path);
    }
}