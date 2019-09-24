using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
    public class Add : MathInstructionBase
    {
        public Add(OperandType first, OperandType second, OperandType third) : base(3, first, second, third)
        { }

        protected override Word Calculate(Word a, Word b)
        {
            unchecked
            {
                return new Word(a.ToUInt() + b.ToUInt());
            }
        }
    }
}