namespace VirtualMachine.SimpleAssembler
{
	interface IParser
	{
		Token[] Parse(string code);
	}
}