namespace VirtualMachine.SimpleAssembler
{
	public class Token
	{
		public Token(int line, TokenType type, string value)
		{
			Line = line;
			Type = type;
			Value = value;
		}

		public int Line { get; }
		public TokenType Type { get; }
		public string Value { get; }
	}
}