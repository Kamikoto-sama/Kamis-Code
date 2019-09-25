using System;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using VirtualMachine.Core.Debugger.Model;

namespace VirtualMachine.Core.Debugger.Client
{
	public class DebuggerClient
	{
		private readonly IHttpClient httpClient;

		public DebuggerClient(IHttpClient httpClient) => this.httpClient = httpClient;

		public Task<DebugMode> GetDebugModeAsync() => Get<DebugMode>("GetDebugMode");
        public Task SetDebugModeAsync(DebugMode mode) => Post("SetDebugMode", mode);

        public Task AddBreakPointAsync(BreakPointDto bp) => Post("AddBreakPoint", bp);
        public Task RemoveBreakPointAsync(string name) => Post("RemoveBreakPoint", name);
        public Task<BreakPointDto[]> GetBreakPointsAsync() => Get<BreakPointDto[]>("GetBreakPoints");

        public Task<bool> IsPausedAsync() => Get<bool>("IsPaused");
        public Task ContinueAsync() => Post("Continue", "VOID");

        public Task<uint> ReadIpAsync() => Get<uint>("ReadIp");
        public Task WriteIpAsync(uint ip) => Post("WriteIp", ip);

        public Task<uint> ReadWordAsync(uint address) => Post<uint, uint>("ReadWord", address);
        public Task WriteWordAsync(uint address, uint value) => Post<(uint, uint)>("WriteWord", (address, value));

        private async Task<TResult> Post<TArg, TResult>(string path, TArg arg) => (await Post<TArg>(path, arg).ConfigureAwait(false)).ToObject<TResult>();
        private async Task<JToken> Post<T>(string path, T arg)
        {
            var token = JToken.FromObject(arg);
            var result = await httpClient.PostAsync(path, token).ConfigureAwait(false);
            if (result.Error != null)
                throw new InvalidOperationException(result.Error);
            return result.Value;
        }

		private async Task<T> Get<T>(string path)
		{
			var result = await httpClient.GetAsync(path).ConfigureAwait(false);
            if (result.Error != null)
                throw new InvalidOperationException(result.Error);
            return result.Value.ToObject<T>();
        }
	}
}
