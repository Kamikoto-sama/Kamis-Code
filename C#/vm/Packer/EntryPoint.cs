using System.IO;

namespace Packer
{
    internal class EntryPoint
    {
        public static void Main(string[] args)
        {
            var result = Packer.Pack(args);
            File.WriteAllText("UserCode.cs", result);
        }
    }
}