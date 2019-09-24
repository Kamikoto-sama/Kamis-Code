using Newtonsoft.Json.Linq;

namespace VirtualMachine.Runner.Configuration
{
    public class TypeDescriptor
    {
        public string AssemblyName { get; set; }
        public string TypeName { get; set; }
        public JObject Parameters { get; set; }
    }
}