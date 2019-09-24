using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace VirtualMachine.Debugger.Server.Http
{
	public static class StreamHelper
	{
		public static async Task<byte[]> ReadToEndAsync(this Stream stream)
		{
			var result = new List<byte>();
			var buffer = new byte[1024];
			while (true)
			{
				var read = await stream.ReadAsync(buffer, 0, buffer.Length).ConfigureAwait(false);
				if (read <= 0)
					break;
				result.AddRange(buffer.Take(read));
			}
			return result.ToArray();
		}
	}
}
