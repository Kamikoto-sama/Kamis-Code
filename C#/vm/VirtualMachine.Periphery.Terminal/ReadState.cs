namespace VirtualMachine.Periphery.Terminal
{
	public enum ReadState : uint
	{
		None = 0,
		ReadRequested = 0xA0,
		Reading = 0xA1,
		ReadCompleted = 0xA2
	}
}