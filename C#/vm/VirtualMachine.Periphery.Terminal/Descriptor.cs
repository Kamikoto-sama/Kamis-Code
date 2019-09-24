using System;
using VirtualMachine.Core;

namespace VirtualMachine.Periphery.Terminal
{
	internal class Descriptor<T>
	{
		public const int Size = 4 * Word.Size;

		public Descriptor(Word address, IMemory memory, Func<T, uint> toUint, Func<uint, T> fromUint)
		{
			this.toUint = toUint;
			this.fromUint = fromUint;
			this.address = address;
			this.memory = memory;
		}

		public T State
		{
			get => fromUint(ReadRegister(0).ToUInt());
			set => WriteRegister(0, new Word(toUint(value)));
		}

		public Word BufferAddress
		{
			get => ReadRegister(1);
			set => WriteRegister(1, value);
		}

		public Word BufferLength
		{
			get => ReadRegister(2);
			set => WriteRegister(2, value);
		}

		public Word StringLength
		{
			get => ReadRegister(3);
			set => WriteRegister(3, value);
		}

		private Word ReadRegister(int number) => memory.ReadWord(GetRegisterAddress(number));
		private void WriteRegister(int number, Word value) => memory.WriteWord(GetRegisterAddress(number), value);
		private Word GetRegisterAddress(int number) => address + new Word(Word.Size * number);

		private readonly Word address;
		private readonly IMemory memory;
		private readonly Func<T, uint> toUint;
		private readonly Func<uint, T> fromUint;
	}
}