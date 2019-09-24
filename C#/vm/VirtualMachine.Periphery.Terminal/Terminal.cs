using System;
using System.Threading;
using VirtualMachine.Core;

namespace VirtualMachine.Periphery.Terminal
{
	public class Terminal : IDevice
	{
		public Terminal(uint address)
		{
			readerAddress = new Word(address);
			writerAddress = new Word(address) + new Word(Descriptor<ReadState>.Size);
		}

		public void Run(IMemory memory)
		{
			while (true)
			{
				reader.Handle(new Descriptor<ReadState>(readerAddress, memory, s => (uint) s, v => (ReadState) v), memory);
				writer.Handle(new Descriptor<WriteState>(writerAddress, memory, s => (uint) s, v => (WriteState) v), memory);

				Thread.Sleep(Delay);
			}
		}

		private readonly Reader reader = new Reader();
		private readonly Writer writer = new Writer();

		private readonly Word readerAddress;
		private readonly Word writerAddress;

		private static readonly TimeSpan Delay = TimeSpan.FromMilliseconds(100);
	}
}
