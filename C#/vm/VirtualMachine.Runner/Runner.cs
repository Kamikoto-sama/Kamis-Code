using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using Newtonsoft.Json;
using VirtualMachine.Core;
using VirtualMachine.CPU;
using VirtualMachine.Runner.Configuration;

namespace VirtualMachine.Runner
{
    public class Runner
    {
        private const string ShowStackTraceParam = "--verbose-error";

        private static Runner Instance;

        public static void Main(string[] args)
        {
            var memoryFileName = args.FirstOrDefault(s => !ShowStackTraceParam.Equals(s, StringComparison.InvariantCultureIgnoreCase));
            var showStackTrace = args.Any(s => ShowStackTraceParam.Equals(s, StringComparison.InvariantCultureIgnoreCase));

            Instance = new Runner(memoryFileName, showStackTrace);
            Instance.Main();
        }

        public void Main()
        {
            var configurationJson = File.ReadAllText("vm.json", Encoding.UTF8);
            var configuration = JsonConvert.DeserializeObject<VirtualMachineConfiguration>(configurationJson);

            var builder = new TypeDescriptorBuilder();
            var instructionSet = builder.Build<IInstructionSet>(configuration.InstructionSet);
            var debugger = builder.Build<ISupervisor>(configuration.Supervisor);

            var cpu = builder.Build<ICpu>(configuration.Cpu, instructionSet, debugger);
            var memory = builder.Build<IMemory>(configuration.Memory);
            var devices = configuration.Devices.Select(d => builder.Build<IDevice>(d)).ToArray();

            if (memoryFileName != null)
            {
                Console.WriteLine($"Loading memory from {memoryFileName}");
                FillMemoryFromFile(memory, memoryFileName);
            }

            Console.WriteLine("Starting devices");

            foreach (var device in devices)
            {
                RunDevice(device, memory);
            }

            Console.WriteLine("Starting cpu\n");

            try
            {
                cpu.Run(memory);
            }
            catch (CpuException e)
            {
                Report(e);
            }
            catch (Exception e)
            {
                Report(e);
            }
        }

        private Runner(string memoryFileName, bool showStackTrace)
        {
            this.memoryFileName = memoryFileName;
            this.showStackTrace = showStackTrace;
        }

        private void RunDevice(IDevice device, IMemory memory)
        {
            var thread = new Thread(() => device.Run(memory))
            {
                IsBackground = true
            };
            thread.Start();
        }

        private void Report(CpuException e)
        {
            Console.WriteLine("Unhandled CPU exception");
            Console.WriteLine($"IP={e.Ip} OpCode={e.OpCode}");
            Console.WriteLine($"Message: {e.Message}");
            Console.WriteLine(showStackTrace
                ? e.StackTrace
				: $"For show stack trace run with parameter {ShowStackTraceParam}");
        }

        private void Report(Exception e)
        {
            Console.WriteLine("Unhandled exception");
            Console.WriteLine($"Message: {e.Message}");
            Console.WriteLine(showStackTrace
                ? e.StackTrace
                : $"For show stack trace run with parameter {ShowStackTraceParam}");
        }

        private void FillMemoryFromFile(IMemory memory, string fileName)
        {
            var data = File.ReadAllBytes(fileName);
            for (var i = 0; i < data.Length; i+=Word.Size)
            {
                var word = new Word(data[i], data[i + 1], data[i + 2], data[i + 3]);
                memory.WriteWord(new Word(i), word);
            }
        }

        private readonly string memoryFileName;
        private readonly bool showStackTrace;
    }
}
