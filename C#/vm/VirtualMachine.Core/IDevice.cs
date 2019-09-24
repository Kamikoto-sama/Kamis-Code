namespace VirtualMachine.Core
{
    public interface IDevice
    {
        void Run(IMemory memory);
    }
}