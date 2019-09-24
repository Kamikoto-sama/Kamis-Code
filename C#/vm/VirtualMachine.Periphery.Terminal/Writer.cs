using System;
using System.Text;
using VirtualMachine.Core;

namespace VirtualMachine.Periphery.Terminal
{
	internal class Writer
	{
		public void Handle(Descriptor<WriteState> descriptor, IMemory memory)
		{
			if (descriptor.State == WriteState.WriteRequested)
			{
				var bytes = memory.ReadString(descriptor.BufferAddress, descriptor.StringLength);
				var line = Encoding.ASCII.GetString(bytes);
				Console.WriteLine(line);

				descriptor.State = WriteState.WriteCompleted;
			}
		}
	}
}