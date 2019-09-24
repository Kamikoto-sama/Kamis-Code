using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
    public class Sub : MathInstructionBase
    {
        public Sub(OperandType first, OperandType second, OperandType third) : base(4, first, second, third)
        { }

        protected override Word Calculate(Word a, Word b)
        {
            unchecked
            {
                return new Word(a.ToUInt() - b.ToUInt());
            }
        }
    }
}