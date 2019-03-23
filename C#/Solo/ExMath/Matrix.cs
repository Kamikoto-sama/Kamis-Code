using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using func_rocket;

namespace ExMath
{
    public class Matrix: IEnumerable<double>
    {
        public double[,] Values { get; }
        public int RowCount => Values.GetLength(0);
        public int ColumnCount => Values.GetLength(1);

        public double this[int i, int j]
        {
            get => Values[i, j];
            set => Values[i, j] = value;
        }

        public Matrix(double[,] values) => Values = values;
        
        public Matrix(Matrix matrix) => Values = (double[,])matrix.Values.Clone();

        public Matrix(Vector vector) => Values = new[,] {{vector.X, vector.Y}};

        public Matrix(int rowCount, int columnCount, double value=0)
        {
            var values = new double[rowCount, columnCount];
            Values = GetNewValues(values, (i, j) => value);
        }
        
        public Matrix Clone() => new Matrix((double[,])Values.Clone());

        public void PrintInLine()
        {
            Console.Write("( ");
            for (var i = 0; i < RowCount; i++)
            {
                Console.Write("{ ");
                for (var j = 0; j < ColumnCount; j++)
                    Console.Write(Values[i, j] + " ");
                Console.Write("} ");
            }
            Console.Write(")");
        }

        public static Matrix RandomMatrix()
        {
            throw new NotImplementedException();
        }

        public Matrix Rotate2D(double angle)
        {
            if(ColumnCount != 2)
                throw new Exception("This matrix must have 2 columns");
            var rotateMatrix = new[,]
            {
                {Math.Cos(angle), -Math.Sin(angle)},
                {Math.Sin(angle), Math.Cos(angle)}
            };
            return this * new Matrix(rotateMatrix);
        }

        public Matrix Rotate3D(double angle)
        {
            var rotateMatrix = new[,]
            {
                {1 , 0 , 0},
                {0, Math.Cos(angle), -Math.Sin(angle)},
                {0, Math.Sin(angle), Math.Cos(angle)}
            };
            return this * new Matrix(rotateMatrix);
        }
        
        public Matrix Transpose()
        {
            var newValues = GetNewValues(Values, (i, j) => this[j, i]);
            return new Matrix(newValues);
        }

        public Vector ToVector() => new Vector(this[0, 0], this[0, 1]);

        private static double[,] GetNewValues(double[,] values, 
            Func<int, int, double> operation)
        {
            var newValues = new double[values.GetLength(0), values.GetLength(1)];
            for (var i = 0; i < values.GetLength(0); i++)
            for (var j = 0; j < values.GetLength(1); j++)
                newValues[i, j] = operation(i, j);
            return newValues;
        }

        public static Matrix operator ^(Matrix matrix, int power)
        {
            var result = matrix.Clone();
            for (var i = 1; i < power; i++) result *= matrix;
            return result;
        }
        
        public static Matrix operator +(Matrix left, Matrix right)
        {
            var rows = left.RowCount;
            var columns = left.ColumnCount;
            if(rows != right.RowCount || columns != right.ColumnCount)
                throw new Exception("Matrix sizes aren't equal");
            
            var newValues = GetNewValues(left.Values, 
                (i, j) => left[i, j] + right[i, j]);
            return new Matrix(newValues);
        }

        public static Matrix operator -(Matrix left, Matrix right) => left + right * -1;
        
        public static Matrix operator *(Matrix matrix, double value)
        {
            var newValues = GetNewValues(matrix.Values, 
                (i, j) => matrix[i, j] * value);
            return new Matrix(newValues);
        }

        public static Matrix operator *(double value, Matrix matrix) => matrix * value;

        public static Matrix operator *(Matrix left, Matrix right)
        {
            var rowCount = right.RowCount;
            if(left.ColumnCount != rowCount)
                throw new Exception("left.ColumnCount must " +
                                    "be equal to right.RowCount");

            var newValues = new double[rowCount, left.ColumnCount];
            var columnCount = right.ColumnCount;
            for (int i = 0, j; i < left.RowCount * right.ColumnCount; i++)
            {
                var cellValue = 0.0;
                for (j = 0; j < columnCount; j++)
                    cellValue += left[i / columnCount, j] * right[j, i % rowCount];

                newValues[i / columnCount, i % columnCount] = cellValue;
            }
            
            return new Matrix(newValues);
        }

        public static Matrix operator /(Matrix matrix, double value)
        {
            return matrix * (1 / value);
        }

        public static Matrix operator /(double value, Matrix matrix) => matrix / value;

        public static bool operator ==(Matrix left, Matrix right)
        {
            if (ReferenceEquals(null, left) && ReferenceEquals(null, right))
                return true;
            return !ReferenceEquals(null, left) && left.Equals(right);
        }

        public static bool operator !=(Matrix left, Matrix right) => !(left == right);

        public IEnumerator<double> GetEnumerator()
        {
            return Values.Cast<double>().GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }

        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            return obj is Matrix matrix && Equals(matrix);
        }

        protected bool Equals(Matrix matrix)
        {
            if (ReferenceEquals(null, matrix)) return false;
            for (var i = 0; i < matrix.RowCount; i++)
            for (var j = 0; j < matrix.ColumnCount; j++)
                if (Math.Abs(matrix[i, j] - this[i, j]) > float.Epsilon)
                    return false;
            return true;
        }

        public override int GetHashCode()
        {
            unchecked
            {
                var result = 0;
                for (var i = 0; i < RowCount; i++)
                for (var j = 0; j < ColumnCount; j++)
                {
                    result = result ^ Values[i, j].GetHashCode()
                             * (i + j) * (Values[i, j] > 0 ? 7 : 3);
                }
                return result;
            }
        }

        public override string ToString()
        {
            var lines = new StringBuilder[RowCount];
            var maxLength = 0;
            for (var i = 0; i < RowCount; i++)
            {
                lines[i] = new StringBuilder();
                lines[i].Append("| ");
                for (var j = 0; j < ColumnCount; j++)
                    lines[i].Append(Values[i, j] + " ");
                if (lines[i].Length > maxLength) maxLength = lines[i].Length;
            }
            var result = lines
                .Select(line => line
                    .Append(new string(' ', maxLength - line.Length) + "|"));
            return string.Join("\n", result);
        }
    }
}