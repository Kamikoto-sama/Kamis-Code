using VirtualMachine.Core;

namespace VirtualMachine.Periphery.Terminal
{
	internal static class MemoryHelper
	{
		public static void WriteString(this IMemory memory, Word address, byte[] value)
		{
			for (var i = 0; i < value.Length; i++)
				memory.WriteByte(address + new Word(i), value[i]);
		}

		public static byte[] ReadString(this IMemory memory, Word address, Word length)
		{
			var result = new byte[length.ToInt()];

			for (var i = 0U; i < length.ToUInt(); i++)
				result[i] = memory.ReadWord(address + new Word(i)).First;

			return result;
		}

		private static void WriteByte(this IMemory memory, Word address, byte value)
		{
			var old = memory.ReadWord(address);
			memory.WriteWord(address, new Word(value, old.Second, old.Third, old.Fourth));
		}
	}
}