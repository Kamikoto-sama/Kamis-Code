namespace VirtualMachine.Periphery.Terminal
{
	public enum WriteState : uint
	{
		None = 0,
		WriteRequested = 0xB0,
		WriteCompleted = 0xB2
	}
}