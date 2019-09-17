using System;
using System.Collections.Generic;

namespace GitTask
{
    public class Git
    {
        private int _commitNumber;
        private readonly int[] _fileStates;
        private readonly List<int> _changedFiles = new List<int>();
        private readonly List<Commit> _commitsHistory = new List<Commit>();
        
        public Git(int filesCount) => _fileStates = new int[filesCount];

        public void Update(int fileNumber, int value)
        {
            if (value == _fileStates[fileNumber])
                return;
            _fileStates[fileNumber] = value;
            _changedFiles.Add(fileNumber);
        }

        public int Commit()
        {
            var newCommit = new Commit();
            foreach (var fileNumber in _changedFiles)
                newCommit.Add(fileNumber, _fileStates[fileNumber]);
            
            _commitsHistory.Add(newCommit);
            _changedFiles.Clear();
            return _commitNumber++;
        }

        public int Checkout(int commitNumber, int fileNumber)
        {
            if (commitNumber < 0 || commitNumber >= _commitsHistory.Count)
                throw new ArgumentException("There is no such commit");
            
            var currentCommit = _commitsHistory[commitNumber];
            while (commitNumber >= 0)
            {
                if (currentCommit.TryGetFileValue(fileNumber, out var value))
                    return value;
                commitNumber--;
            }
            return _fileStates[fileNumber];
        }
    }

    public class Commit
    {
        private readonly List<int> _fileValues = new List<int>();
        private readonly List<int> _fileNumbers = new List<int>();

        public void Add(int fileNumber, int fileValue)
        {
            _fileValues.Add(fileValue);
            _fileNumbers.Add(fileNumber);
        }

        public bool TryGetFileValue(int fileNumber, out int fileValue)
        {
            for (var fileIndex = 0; fileIndex < _fileNumbers.Count; fileIndex++)
            {
                if (_fileNumbers[fileIndex] != fileNumber) continue;
                fileValue = _fileValues[fileIndex];
                return true;
            }
            fileValue = 0;
            return false;
        }
    }
}