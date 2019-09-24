namespace VirtualMachine.Runner.Configuration
{
    public class VirtualMachineConfiguration
    {
        public TypeDescriptor InstructionSet { get; set; }
        public TypeDescriptor Supervisor { get; set; }
        public TypeDescriptor Cpu { get; set; }
        public TypeDescriptor Memory { get; set; }
        public TypeDescriptor[] Devices { get; set; }
    }
}