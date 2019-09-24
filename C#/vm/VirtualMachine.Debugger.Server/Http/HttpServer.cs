using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using VirtualMachine.Core.Debugger;
using VirtualMachine.Core.Debugger.Server;

namespace VirtualMachine.Debugger.Server.Http
{
	public class HttpServer : IHttpServer
	{
		public HttpServer(string host, ushort port)
		{
			this.host = host;
			this.port = port;
		}

		public void AddHandler(string path, HttpMethod method, Action handler)
		{
			AddHandler(path, method, _ => handler());
		}

		public void AddHandler(string path, HttpMethod method, Action<JToken> handler)
		{
			AddHandler(path, method, a =>
			{
				handler(a);
				return JToken.FromObject("VOID");
			});
		}

		public void AddHandler(string path, HttpMethod method, Func<JToken> handler)
		{
			AddHandler(path, method, _ => handler());
		}

		public void AddHandler(string path, HttpMethod method, Func<JToken, JToken> handler)
		{
			AddHandler(path, method, a =>
			{
				try
				{
					return Result.Success(handler(a));
				}
				catch (Exception e)
				{
					return Result.Fail<JToken>(e.ToString());
				}
			});
		}

		public void AddHandler(string path, HttpMethod method, Func<Result<JToken>> handler)
		{
			AddHandler(path, method, _ => handler());
		}

		public void AddHandler(string path, HttpMethod method, Func<JToken, Result<JToken>> handler)
		{
			AddHandler(path, method, a =>
			{
				try
				{
					return Task.FromResult(handler(a));
				}
				catch (Exception e)
				{
					return Task.FromException<Result<JToken>>(e);
				}
			});
		}

		public void AddHandler(string path, HttpMethod method, Func<Task<Result<JToken>>> handler)
		{
			AddHandler(path, method, _ => handler());
		}

		public void AddHandler(string path, HttpMethod method, Func<JToken, Task<Result<JToken>>> handler)
		{
			async Task<HttpStatusCode> Handle(HttpListenerContext context)
			{
				if (!string.Equals(method.ToString(), context.Request.HttpMethod, StringComparison.CurrentCultureIgnoreCase))
				{
					return HttpStatusCode.BadRequest;
				}

				var requestBytes = await context.Request.InputStream.ReadToEndAsync().ConfigureAwait(false);
				var requestJson = Encoding.UTF8.GetString(requestBytes);
				var request = JToken.Parse(string.IsNullOrWhiteSpace(requestJson) ? "null": requestJson);

				var response = await handler(request).ConfigureAwait(false);
				
				var responseJson = JsonConvert.SerializeObject(response);
				var responseBytes = Encoding.UTF8.GetBytes(responseJson);

				context.Response.OutputStream.Write(responseBytes, 0, responseBytes.Length);

				return HttpStatusCode.OK;
			}

			if (started)
				throw new InvalidOperationException();

			lock (handler)
			{
				if (started)
					throw new InvalidOperationException();

				listeners.Add(path, new Listener(host, port, path, Handle));
			}
		}

		public void Start()
		{
			if(started)
				throw new InvalidOperationException("Already started");

			lock (listeners)
			{
				if (started)
					throw new InvalidOperationException("Already started");

				started = true;
				foreach (var listener in listeners)
					listener.Value.Listen();
			}
		}

		public void Dispose()
		{
			foreach (var listener in listeners)
			{
				try
				{
					listener.Value.Dispose();
				}
				catch
				{
					// ignored
				}
			}
		}

		private bool started;

		private readonly string host;
		private readonly ushort port;
		private readonly Dictionary<string, Listener> listeners = new Dictionary<string, Listener>();
	}
}