@echo off

echo ===========================
echo QueueCTL Test Started
echo ===========================

python main.py enqueue job1 "echo Hello"
python main.py enqueue job2 "echo World"
python main.py enqueue fail1 "wrongcommand"

echo.
echo ===== All Jobs =====
python main.py list

echo.
echo ===== Queue Status =====
python main.py status

echo.
echo ===== Start Worker =====
python main.py worker start --count 2

echo.
echo ===== Queue Status =====
python main.py status

echo.
echo ===== DLQ =====
python main.py dlq list

pause