using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace VirtualMachine.Runner.Configuration
{
    public class TypeDescriptorBuilder
    {
        public T Build<T>(TypeDescriptor descriptor, params object[] parameters)
        {
            try
            {

                var assembly = GetOrLoadAssembly(new FileInfo(descriptor.AssemblyName));
                var type = assembly.GetType(descriptor.TypeName);

                if (type == null)
                    throw new InvalidOperationException($"Type '{descriptor.TypeName}' not found in assembly {descriptor.AssemblyName}");

                if (!typeof(T).IsAssignableFrom(type))
                    throw new InvalidOperationException($"Type '{descriptor.TypeName}' is not derived from {typeof(T).FullName}");

                if (type.GetConstructors().Length != 1)
                    throw new InvalidOperationException($"Constructor overloading not supported");
                var constructor = type.GetConstructors().Single();
                
                if (parameters == null || !parameters.Any())
                {
                    parameters = constructor.GetParameters()
                        .Select(p => DeserializeParam(descriptor.Parameters, p.Name, p.ParameterType))
                        .ToArray();
                }

                return (T) constructor.Invoke(parameters);
            }
            catch (Exception e)
            {
                throw new InvalidOperationException($"Cant build instance of type '{descriptor.TypeName}'", e);
            }
        }

        private static object DeserializeParam(JObject parameters, string name, Type paramType)
        {
            var value = parameters.ContainsKey(name)
                ? parameters[name]
                : parameters.Cast<JProperty>().FirstOrDefault(p => p.Name.Equals(name, StringComparison.InvariantCultureIgnoreCase))?.Value;

            if (value == null)
                throw new InvalidOperationException($"Parameter {name} not found in\n{parameters.ToString(Formatting.Indented)}");

            return value.ToObject(paramType) ?? throw new InvalidOperationException($"Cant deserialize json to {paramType.FullName}:\n{value.ToString(Formatting.Indented)}");
        }

        private static Assembly GetOrLoadAssembly(FileInfo file)
        {
            var name = AssemblyName.GetAssemblyName(file.FullName);
            var assembly = AppDomain.CurrentDomain
                .GetAssemblies()
                .FirstOrDefault(a => a.FullName.Equals(name.FullName));
            return assembly ?? Assembly.LoadFile(file.FullName);
        }
    }
}