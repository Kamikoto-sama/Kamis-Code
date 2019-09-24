using VirtualMachine.Core;

namespace VirtualMachine.Debugger.Client.Console.Helpers
{
	public static class WordHelper
	{
		public static string ToLHex(this uint w) => w.ToHex(false);

		public static string ToBHex(this uint w) => w.ToHex(true);

		private static string ToHex(this uint v, bool bigEndian)
		{
			var word = new Word(v);
			return bigEndian
				? $"{word.HighHigh:X2} {word.HighLow:X2} {word.LowHigh:X2} {word.LowLow:X2}" 
				: $"{word.LowLow:X2} {word.LowHigh:X2} {word.HighLow:X2} {word.HighHigh:X2}";
		}
	}
}