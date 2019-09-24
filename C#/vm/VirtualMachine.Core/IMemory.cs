namespace VirtualMachine.Core
{
    public interface IMemory : IReadOnlyMemory
    {
        void WriteWord(Word address, Word value);

        bool CompareExchange(Word address, Word expectedValue, Word value, out Word oldValue);
    }
}