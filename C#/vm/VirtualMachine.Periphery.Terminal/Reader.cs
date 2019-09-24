using System;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using VirtualMachine.Core;

namespace VirtualMachine.Periphery.Terminal
{
	internal class Reader
	{
		public void Handle(Descriptor<ReadState> descriptor, IMemory memory)
		{
			if (readTask != null)
			{
				if (readTask.IsCompleted)
				{
					readTask = null;
					descriptor.State = ReadState.ReadCompleted;
				}
				else
				{
					descriptor.State = ReadState.Reading;
				}
			}
			else if (descriptor.State == ReadState.ReadRequested)
			{
				descriptor.State = ReadState.Reading;

				var buffer = descriptor.BufferAddress;
				var bufferLength = descriptor.BufferLength;

				readTask = Task.Run(() => Read(descriptor, memory, buffer, bufferLength));
			}
		}

		private static void Read(Descriptor<ReadState> descriptor, IMemory memory, Word buffer, Word bufferLength)
		{
			var line = Console.ReadLine();
			var bytes = Encoding.ASCII.GetBytes(line).Take(bufferLength.ToInt()).ToArray();
			memory.WriteString(buffer, bytes);
			descriptor.StringLength = new Word(bytes.Length);
		}

		private Task readTask;
	}
}