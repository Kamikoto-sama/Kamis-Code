namespace VirtualMachine.CPU.InstructionSet
{
    public enum OperandType : uint
    {
        Ignored = 0,
        Constant = 1,
        Address = 2,
        AddressOfAddress = 3
    }
}