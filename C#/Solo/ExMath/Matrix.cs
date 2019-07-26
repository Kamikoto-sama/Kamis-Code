using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ExMath
{
    public class Matrix: IEnumerable<double>
    {
        public double[,] Values { get; }
        public int RowCount => Values.GetLength(0);
        public int ColumnCount => Values.GetLength(1);
        public int Count => Values.Length;
        public double Determinant
        {
            get
            {
                if(RowCount != ColumnCount)
                    throw new Exception("Matrix must be square");
                return GetDeterminant(this);
            }
        }
        public Matrix Inverse => GetInverseMatrix(this);

        public double this[int i]
        {
            get => this[i / ColumnCount, i % ColumnCount];
            set => this[i / ColumnCount, i % ColumnCount] = value;
        }
        public double this[int i, int j]
        {
            get => Values[i, j];
            set => Values[i, j] = value;
        }

        public Matrix(double[,] values)
        {
            if(values == null || values.Length == 0)
                throw new Exception("Matrix can't be empty or null");
            Values = (double[,]) values.Clone();
        }

        public Matrix(IEnumerable<double> array, int columnCount)
        {
            var values = array.ToArray();
            if(values.Length % columnCount != 0)
                throw new Exception("Value count must be a multiple " +
                                    "of the number of columns");
            var newValues = new double[values.Length / columnCount, columnCount];
            for (var i = 0; i < values.Length; i++)
                newValues[i / columnCount, i % columnCount] = values[i];
            Values = newValues;
        }    

        public Matrix(Matrix matrix) => Values = (double[,])matrix.Values.Clone();

        public Matrix(Vector vector) => Values = new[,] {{vector.X, vector.Y}};

        public Matrix(int rowCount, int columnCount, double value=0)
        {
            var values = new double[rowCount, columnCount];
            Values = ParseValues(rowCount, columnCount, (i, j) => value);
        }
        
        public Matrix Clone() => new Matrix((double[,])Values.Clone());

        public static Matrix UnitMatrix(int size)
        {
            var values = new double[size, size];
            return new Matrix(ParseValues(size, size, (i, j) => i == j ? 1 : 0));
        }

        public static Matrix RandomMatrix(int rowMax=5, int columnMax=5,
             double valueMax=100, double valueMin=-100, int rowMin=1, int columnMin=1)
        {
            if(rowMax < 1 || rowMin < 1 || columnMax < 1 || columnMin < 1)
                throw new Exception("Column and row count must be" +
                                    "grater than 0");
            if(rowMax < rowMin || columnMax < columnMin || valueMax < valueMin)
                throw new Exception("Max value must be grater than min");
            
            var random = new Random();
            var rowCount = random.Next(rowMin, rowMax);
            var columnCount = random.Next(columnMin, columnMax);
            var newValues = ParseValues(rowCount, columnCount,
                (i, j) => Math.Round(random.NextDouble(valueMin, valueMax), 2));
            return new Matrix(newValues);
        }

        public static Matrix RandomMatrix(double maxValue, int size, 
            double minValue = -100)
        {
            return RandomMatrix(size, size, maxValue, 
                minValue, size, size);
        }

        public static Matrix RandomIntMatrix(int size, int maxValue, 
            int minValue = -100)
        {
            var rnd = new Random();
            var newValues = ParseValues(size, size, 
                (i, j) => rnd.Next(minValue, maxValue));
            return new Matrix(newValues);
        }
        
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
            if(ColumnCount != 3)
                throw new Exception("This matrix must have 3 columns");
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
            var newValues = ParseValues(RowCount, ColumnCount, (i, j) => this[j, i]);
            return new Matrix(newValues);
        }

        public Vector ToVector2D()
        {
            if(RowCount != 1 && ColumnCount != 2)
                throw new Exception("Vector must have values at [0, 0] and [0, 1]");
            return new Vector(this[0, 0], this[0, 1]);
        }

        public bool Contains(double value) => Values.Cast<double>().Contains(value);

        public double[] GetRow(int rowNumber) => ParseLine(ColumnCount, 
            i => this[rowNumber, i]);
        
        public double[] GetColumn(int columnNumber) => ParseLine(RowCount, 
            i => this[i, columnNumber]);

        public Matrix SwapRows(int row1, int row2)
        {
            var newValues = (double[,]) Values.Clone();
            for (var i = 0; i < ColumnCount; i++)
            {
                var temp = newValues[row2, i];
                newValues[row2, i] = newValues[row1, i];
                newValues[row1, i] = temp;
            }
            return new Matrix(newValues);
        }
        
        public Matrix SwapColumns(int column1, int column2)
        {
            var newValues = (double[,]) Values.Clone();
            for (var i = 0; i < RowCount; i++)
            {
                var temp = newValues[i, column2];
                newValues[i, column2] = newValues[i, column1];
                newValues[i, column1] = temp;
            }
            return new Matrix(newValues);
        }
        
        public Matrix RemoveRow(int row)
        {
            var newValues = Values
                .Cast<double>()
                .Where((d, i) => i / ColumnCount != row)
                .ToArray();
            return new Matrix(newValues, ColumnCount);
        }
        
        public Matrix RemoveColumn(int column)
        {
            var newValues = this
                .Where((d, i) => i % ColumnCount != column)
                .ToArray();
            return new Matrix(newValues, ColumnCount);
        }

        public Matrix GetMinor(int row, int column) => GetMinor(this, row, column);

        public double GetMainMinor(int number)
        {
            if(RowCount != ColumnCount)
                throw new Exception("Matrix must be square");
            if(number > RowCount)
                throw new Exception("Minor number is grater than matrix order");
            if(number <= 0)
                throw new Exception("Minor number must be >= 1");
            return GetRange(0, 0, number - 1, number - 1).Determinant;
        }

        public Matrix GetRange(int rowStart, int columnStart, 
            int rowEnd, int columnEnd)
        {
            if(rowEnd < rowStart || columnEnd < columnStart)
                throw new Exception("End values must be grater than start");

            var newValues = new double[columnEnd - columnStart + 1, 
                rowEnd - rowStart + 1];
            for (var i = rowStart; i <= rowEnd; i++)
            for (var j = columnStart; j <= columnEnd; j++)
                newValues[i - rowStart, j - columnStart] = this[i, j];
            return newValues.ToMatrix();
        }

        public Matrix Round(int decimals)
        {
            var newValues = ParseValues(RowCount, ColumnCount,
                (i, j) => Math.Round(this[i, j], decimals));
            return new Matrix(newValues);
        }

        public Matrix Reset()
        {
            if(RowCount != ColumnCount)
                throw new Exception("Matrix must be square");
            return UnitMatrix(RowCount);
        }
        
        private static Matrix GetInverseMatrix(Matrix matrix)
        {
            var determinant = matrix.Determinant;
            if(Math.Abs(determinant) <= float.Epsilon)
                throw new Exception("Determinant is 0");
            
            var colCount = matrix.ColumnCount;
            var minors = GetMinorsMatrix(matrix, colCount);
            var algAdds = ParseValues(colCount, colCount,
                (i, j) => i - j == 1 || j - i == 1 ? -minors[i, j] : minors[i, j])
                .ToMatrix();
            return new Matrix(algAdds.Transpose() / determinant);
        }

        private static Matrix GetMinorsMatrix(Matrix matrix, int colCount)
        {
            var minors = matrix.Select((d, i) =>
            {
                var row = i / colCount;
                var column = i % colCount;
                return matrix.GetMinor(row,column).Determinant;
            });
            return minors.ToMatrix(colCount);
        }

        private static double[,] ParseValues(int rowCount, int columnCount,
            Func<int, int, double> operation)
        {
            var newValues = new double[rowCount, columnCount];
            for (var i = 0; i < rowCount; i++)
            for (var j = 0; j < columnCount; j++)
                newValues[i, j] = operation(i, j);
            return newValues;
        }

        private static double[] ParseLine(int count, Func<int, double> parse)
        {
            var newValues = new double[count];
            for (var i = 0; i < count; i++)
                newValues[i] = parse(i);
            return newValues;
        }

        private static double GetDeterminant(Matrix matrix, double result=0)
        {
            if (matrix.RowCount == 1)
                return matrix[0, 0];
            var rowLength = matrix.ColumnCount;
            for (var i = 0; i < rowLength; i++)
            {
                var minor = matrix.GetMinor(0, i);
                result += GetDeterminant(new Matrix(minor, rowLength - 1))
                          * matrix[0, i] * (i % 2 == 0 ? 1 : -1);
            }
            return result;
        }

        private static Matrix GetMinor(Matrix matrix, int row, int column)
        {
            if(matrix.RowCount != matrix.ColumnCount)
                throw new Exception("Matrix must be square");
            if (matrix.RowCount == 1)
                return matrix;
            var newValues = matrix
                .Where((d, i) => i / matrix.ColumnCount != row
                                 && i % matrix.ColumnCount != column);
            return new Matrix(newValues, matrix.ColumnCount -1);
        }

        public static Matrix operator ^(Matrix matrix, int power)
        {
            if(power < 1 && power != -1)
                throw new Exception("Power must be natural or -1");
            
            if (power == -1)
                return matrix.Inverse;
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
            
            var newValues = ParseValues(left.RowCount, left.ColumnCount,
                (i, j) => left[i, j] + right[i, j]);
            return new Matrix(newValues);
        }

        public static Matrix operator -(Matrix left, Matrix right) => left + right * -1;
        
        public static Matrix operator *(Matrix matrix, double value)
        {
            var newValues = ParseValues(matrix.RowCount, matrix.ColumnCount,
                (i, j) => matrix[i, j] * value);
            return new Matrix(newValues);
        }

        public static Matrix operator *(double value, Matrix matrix) => matrix * value;

        public static Matrix operator *(Matrix left, Matrix right)
        {
            if(left.ColumnCount != right.RowCount)
                throw new Exception("left.ColumnCount must " +
                                    "be equal to right.RowCount");

            var rColCount = right.ColumnCount;
            var newValues = new double[left.RowCount, rColCount];
            for (int i = 0, j; i < left.RowCount * rColCount; i++)
            {
                var cellValue = 0.0;
                for (j = 0; j < rColCount; j++)
                    cellValue += left[i / rColCount, j] * right[j, i % right.RowCount];
                newValues[i / rColCount, i % rColCount] = cellValue;
            }
            
            return new Matrix(newValues);
        }

        public static Matrix operator /(Matrix matrix, double value)
        {
            return matrix * (1 / value);
        }

        public static Matrix operator /(double value, Matrix matrix) => matrix / value;

        public static Matrix operator /(Matrix left, Matrix right)
            => left * right.Inverse;

        public static bool operator ==(Matrix left, Matrix right)
        {
            if (ReferenceEquals(null, left) && ReferenceEquals(null, right))
                return true;
            return !ReferenceEquals(null, left) && left.Equals(right);
        }

        public static bool operator !=(Matrix left, Matrix right) => !(left == right);

        public static implicit operator double[,](Matrix matrix) => matrix.Values;
        
        public static implicit operator double[](Matrix matrix) => matrix.ToArray();

        public static implicit operator Vector(Matrix matrix) => matrix.ToVector2D();

        public static implicit operator Matrix(Vector vector) => vector.ToMatrix();
        
        public static implicit operator Matrix(double[,] array) => array.ToMatrix();

        public IEnumerator<double> GetEnumerator() 
            => Values.Cast<double>().GetEnumerator();

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

    public static class MatrixExtension
    {
        public static Matrix ToMatrix(this double[,] values) => new Matrix(values);

        public static Matrix ToMatrix(this IEnumerable<double> values, int columnCount)
            => new Matrix(values, columnCount);
        
        public static Matrix ToMatrix(this Vector vector) => new Matrix(vector);
    }
}