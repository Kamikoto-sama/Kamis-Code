using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
    public class SAdd : MathInstructionBase
    {
        public SAdd(OperandType first, OperandType second, OperandType third)
            : base(5, first, second, third)
        { }

        protected override Word Calculate(Word a, Word b)
        {
            unchecked
            {
                return new Word(a.ToInt() + b.ToInt());
            }
        }
    }
}