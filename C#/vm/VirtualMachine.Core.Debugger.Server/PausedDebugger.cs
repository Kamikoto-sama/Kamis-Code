using System.Threading;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Server
{
	public class PausedDebugger
	{
		public PausedDebugger(IPauseContext pauseContext)
		{
			Context = pauseContext;
		}

		public Task Continued => continued.Task;
		public readonly IPauseContext Context;

		public void Continue() => continued.SetResult(true);

		private readonly TaskCompletionSource<object> continued = new TaskCompletionSource<object>();
	}
}