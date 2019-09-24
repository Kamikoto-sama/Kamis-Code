using System;
using System.Net;
using System.Threading;
using System.Threading.Tasks;

namespace VirtualMachine.Debugger.Server.Http
{
    public class Listener : IDisposable
    {
        public Listener(string host, uint port, string path, Func<HttpListenerContext, Task<HttpStatusCode>> handler)
        {
	        listener.Prefixes.Add($"http://{host}:{port}/{path?.TrimEnd('/')}/");
			this.handler = handler;
			listenThread = new Thread(ListenLoop) {IsBackground = true};
        }

        public void Listen()
        {
	        listener.Start();
	        listenThread.Start();
        }

        public void Dispose()
        {
	        ((IDisposable) listener)?.Dispose();
        }

        private async void ListenLoop()
        {
            while (true)
            {
	            var context = await listener.GetContextAsync().ConfigureAwait(false);
	            Task.Run(() => Handle(context));
            }
        }

        private async Task Handle(HttpListenerContext context)
        {
	        try
	        {
		        using (var response = context.Response)
		        {
			        try
			        {
				        response.StatusCode = (int) await handler.Invoke(context).ConfigureAwait(false);
			        }
			        catch
			        {
				        response.StatusCode = (int) HttpStatusCode.InternalServerError;
			        }
		        }
	        }
	        catch
	        {
		        // ignored
	        }
        }

        private readonly Thread listenThread;
        private readonly HttpListener listener = new HttpListener();
        private readonly Func<HttpListenerContext, Task<HttpStatusCode>> handler;
    }
}