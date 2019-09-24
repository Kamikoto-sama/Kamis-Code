using System.Collections.Generic;
using VirtualMachine.Core;

namespace VirtualMachine.CPU
{
    public interface IInstructionSet
    {
        IInstruction FindInstruction(Word opCode);

        IEnumerable<IInstruction> GetAll();
    }
}