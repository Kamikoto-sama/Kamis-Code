namespace VirtualMachine.SimpleAssembler
{
	public interface IAssembler
	{
		byte[] Assembly(string code);
	}
}