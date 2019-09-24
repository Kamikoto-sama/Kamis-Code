using System.Threading.Tasks;
using VirtualMachine.Core.Debugger.Client;

namespace VirtualMachine.Debugger.Client.Console
{
    public static class EntryPoint
    {
        public static Task Main()
        {
            var app = new DebuggerApplication(new DebuggerModel(), new CommandSet(), new CommandResultWriterSet());
            return app.RunAsync();
        }
    }
}
