using System;
using System.Linq;
using System.Text;
using VirtualMachine.Core;
using VirtualMachine.Core.Debugger.Client;
using VirtualMachine.Core.Debugger.Client.Commands;
using VirtualMachine.Debugger.Client.Console.Helpers;

namespace VirtualMachine.Debugger.Client.Console.CommandResultWriters
{
    public class ReadMemoryCommandResultWriter : ICommandResultWriter
    {
        private const ConsoleColor InfoZeroColor = ConsoleColor.DarkGray;
        private const ConsoleColor InfoNonZeroColor = ConsoleColor.White;
        private static readonly ConsoleColor[] ValueZeroColors = {ConsoleColor.DarkCyan, ConsoleColor.DarkGreen};
        private static readonly ConsoleColor[] ValueNonZeroColors = {ConsoleColor.Cyan, ConsoleColor.Green};
        
        public Type CommandType => typeof(ReadMemoryCommand);
        
        public void WriteResult(ICommand command)
        {
            var readMemoryCommand = (ReadMemoryCommand) command;
            var (address, rows, columnsCount) = readMemoryCommand.Result;
            
            foreach (var row in rows)
            {
                PrintRow(address, row);
                address += new Word(columnsCount * Word.Size);
            }
        }
        
        private static void PrintRow(Word beginAddress, Word[] words)
        {
            if (!words.Any())
                return;

            var infoColor = words.Any(w => w != Word.Zero) ? InfoNonZeroColor : InfoZeroColor;
            infoColor.Write($"{beginAddress.ToUInt().ToBHex()}\t");
            Print(words, w => w.ToString());
            infoColor.Write("\t|");
            Print(words, w => $"{ToAscii(w.First)}{ToAscii(w.Second)}{ToAscii(w.Third)}{ToAscii(w.Fourth)}");
            infoColor.WriteLine("|");
        }

        private static void Print(Word[] words, Func<Word, string> toString)
        {
            var i = 0;
            foreach (var word in words)
            {
                var colorsCollection = (word == Word.Zero ? ValueZeroColors : ValueNonZeroColors);
                var color = colorsCollection[i++ % colorsCollection.Length];
                color.Write($"{toString(word)} ");
            }
        }

        private static char ToAscii(byte b) => Encoding.ASCII.GetString(new[] {b})[0];
    }
}