namespace JSONSerializer
{
    public static class Serializer
    {
        public static void ToJSON<T>(T obj)
        {
            
        }

        private static void ObjToDict<T>(T obj)
        {
            var type = typeof(T);
            var f = type.GetField("a");
            f.
        }
    }
}