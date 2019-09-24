namespace VirtualMachine.Core
{
    public interface IReadOnlyMemory
    {
        Word ReadWord(Word address);
    }
}