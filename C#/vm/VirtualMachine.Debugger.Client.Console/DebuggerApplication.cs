using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using VirtualMachine.Core.Debugger.Client;
using VirtualMachine.Debugger.Client.Console.CommandResultWriters;
using VirtualMachine.Debugger.Client.Console.Helpers;
using VirtualMachine.Debugger.Client.Console.Http;

namespace VirtualMachine.Debugger.Client.Console
{
    public class DebuggerApplication
    {
        public DebuggerApplication(DebuggerModel model, CommandSet commandSet, CommandResultWriterSet commandResultWriterSet)
        {
            this.model = model;
            this.commandSet = commandSet;
            this.commandResultWriterSet = commandResultWriterSet;
            list = new ListCommand(commandSet.GetAll());
            commandSet.Add(list);
            commandSet.Add(new HelpCommand(commandSet));
            commandSet.Add(new ConnectCommand());
        }

        public async Task RunAsync()
        {
            ConsoleColor.White.WriteLine($"Welcome to Debugger");
            ConsoleColor.White.WriteLine($"Enter {list.Name} for show commands list");

            while (true)
            {
	            ConsoleColor.White.WriteLine();

				var commandName = ConsoleColor.DarkCyan.ReadLine("command");
                if (!commandSet.TryFindCommand(commandName, out var command))
                {
                    ConsoleColor.Red.WriteLine($"Unknown command. Enter {list.Name} for show commands list");
                    continue;
                }

                var parameters = command.ParameterNames.Select(n => ConsoleColor.DarkCyan.ReadLine(n)).ToArray();

                try
                {
                    await command.ExecuteAsync(model, parameters).ConfigureAwait(false);
                    if (commandResultWriterSet.TryFindWriter(command, out var writer))
                    {
                        writer.WriteResult(command);
                    }
                }
                catch (Exception e)
                {
                    ConsoleColor.DarkRed.WriteLine($"Error: {e.GetType().Name}:\n\t{e.Message}");
                    ConsoleColor.DarkRed.WriteLine($"\n{e.StackTrace}");
                }
            }
        }

        private readonly ICommand list;
        private readonly DebuggerModel model;
        private readonly CommandSet commandSet;
        private readonly CommandResultWriterSet commandResultWriterSet;

        private class ListCommand : ICommand
        {
            public ListCommand(IReadOnlyCollection<ICommand> commands) => this.commands = commands;

            public string Name { get; } = "list";
            public string Info { get; } = "Show commands list";
            public IReadOnlyList<string> ParameterNames { get; } = new string[0];

            public Task ExecuteAsync(DebuggerModel model, string[] parameters)
            {
                foreach (var command in commands)
                {
                    ConsoleColor.Cyan.Write(command.Name);
                    ConsoleColor.White.WriteLine($"\t-\t{command.Info}");
                }
                return Task.CompletedTask;
            }

            private readonly IReadOnlyCollection<ICommand> commands;
        }

        private class HelpCommand : ICommand
        {
            private readonly CommandSet commandSet;

            public HelpCommand(CommandSet commandSet) => this.commandSet = commandSet;

            public string Name { get; } = "help";
            public string Info { get; } = "Show command help";
            public IReadOnlyList<string> ParameterNames { get; } = new[] {"command name"};
            public Task ExecuteAsync(DebuggerModel model, string[] parameters)
            {
                if (!commandSet.TryFindCommand(parameters[0], out var command))
                {
                    ConsoleColor.Red.WriteLine("Unknown command");
                    return Task.CompletedTask;
                }

                ConsoleColor.Cyan.Write(command.Name);
                ConsoleColor.White.WriteLine($"\t-\t{command.Info}");

                foreach (var param in command.ParameterNames)
                {
                    ConsoleColor.DarkCyan.WriteLine($"\t{param}");
                }
                
                return Task.CompletedTask;
            }
        }
        
        private class ConnectCommand : ICommand
        {
            public string Name { get; } = "connect";
            public string Info { get; } = "Connect to remote debugger";
            public IReadOnlyList<string> ParameterNames { get; } = new[] {"host", "port"};

            public Task ExecuteAsync(DebuggerModel model, string[] parameters)
            {
                model.Client = new DebuggerClient(new HttpClient(parameters[0], ushort.Parse(parameters[1])));
                return Task.CompletedTask;
            }
        }
    }
}