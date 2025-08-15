from main import LogHandler


name_file1 = "examples_test/example1.log"
name_file2 = "examples_test/example2.log"
wrong_path = "examples_test/wrong.log"



def test_main_avg_with_wrong_path():
    a = LogHandler(file=[wrong_path, ], )
    result = a.main()
    assert result == []


def test_main_avg_with_one_path():
    a = LogHandler(file=[name_file1, ], )
    result = a.main()
    assert result == [
        [0, '/api/homeworks/...', 71, '0.158'],
        [1, '/api/context/...', 21, '0.043'],
        [2, '/api/specializations/...', 6, '0.035'],
        [3, '/api/users/...', 1, '0.072'],
        [4, '/api/challenges/...', 1, '0.056'],
    ]

def test_main_avg_with_two_path():
    a = LogHandler(file=[name_file1,name_file2 ], )
    result = a.main()
    assert result == [
        [0, '/api/homeworks/...', 55312, '0.093'],
        [1, '/api/context/...', 43928, '0.019'],
        [2, '/api/specializations/...', 8335, '0.052'],
        [3, '/api/challenges/...', 1476, '0.078'],
        [4, '/api/users/...', 1447, '0.066'],
    ]

def test_main_min_with_two_path():
    a = LogHandler(file=[name_file1,name_file2 ], report="min")
    result = a.main()
    assert result == [
        [0, '/api/homeworks/...', 55312, '0.000'],
        [1, '/api/context/...', 43928, '0.000'],
        [2, '/api/specializations/...', 8335, '0.004'],
        [3, '/api/challenges/...', 1476, '0.012'],
        [4, '/api/users/...', 1447, '0.020'],
    ]

def test_main_max_with_two_path():
    a = LogHandler(file=[name_file1,name_file2 ], report="max")
    result = a.main()
    assert result == [
        [0, '/api/homeworks/...', 55312, '0.998'],
        [1, '/api/context/...', 43928, '0.988'],
        [2, '/api/specializations/...', 8335, '0.888'],
        [3, '/api/challenges/...', 1476, '0.936'],
        [4, '/api/users/...', 1447, '0.740'],
    ]

def test_main_date_avg_with_two_path():
    a = LogHandler(
        file=[name_file1,name_file2 ],
        report="average",
        date="2025-24-06",
    )
    result = a.main()
    assert result == [
        [0, '/api/homeworks/...', 8921, '0.089', '2025-24-06'],
        [1, '/api/context/...', 6914, '0.018', '2025-24-06'],
        [2, '/api/specializations/...', 1166, '0.052', '2025-24-06'],
        [3, '/api/challenges/...', 212, '0.078', '2025-24-06'],
        [4, '/api/users/...', 206, '0.062', '2025-24-06'],
    ]

def test_main_date_max_with_two_path():
    a = LogHandler(
        file=[name_file1,name_file2 ],
        report="max",
        date="2025-24-06",
    )
    result = a.main()
    assert result == [
        [0, '/api/homeworks/...', 8921, '0.986', '2025-24-06'],
        [1, '/api/context/...', 6914, '0.500', '2025-24-06'],
        [2, '/api/specializations/...', 1166, '0.568', '2025-24-06'],
        [3, '/api/challenges/...', 212, '0.592', '2025-24-06'],
        [4, '/api/users/...', 206, '0.168', '2025-24-06'],
    ]

def test_main_date_min_with_two_path():
    a = LogHandler(
        file=[name_file1,name_file2 ],
        report="min",
        date="2025-24-06",
    )
    result = a.main()
    assert result == [
        [0, '/api/homeworks/...', 8921, '0.000', '2025-24-06'],
        [1, '/api/context/...', 6914, '0.004', '2025-24-06'],
        [2, '/api/specializations/...', 1166, '0.004', '2025-24-06'],
        [3, '/api/challenges/...', 212, '0.016', '2025-24-06'],
        [4, '/api/users/...', 206, '0.020', '2025-24-06'],
    ]