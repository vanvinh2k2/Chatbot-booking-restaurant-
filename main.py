# import asyncio

# async def foo():
#     print("Bắt đầu foo")
#     await asyncio.sleep(1)  # Chờ 1 giây mà không chặn luồng
#     print("Kết thúc foo")

# async def bar():
#     print("Bắt đầu bar")
#     await asyncio.sleep(2)  # Chờ 2 giây mà không chặn luồng
#     print("Kết thúc bar")

# async def main():
#     print("Bắt đầu main")
#     await asyncio.gather(foo(), bar())  # Đợi cả foo và bar hoàn thành
#     print("Kết thúc main")

# asyncio.run(main())

import time

# Mảng chứa các ký tự để tạo hiệu ứng loading
symbols = ['-', '\\', '|', '/']
# Lặp vô hạn để tạo hiệu ứng loading
while True:
    for symbol in symbols:
        # In ra ký tự hiện tại và đặt con trỏ về đầu dòng (\r)
        print(symbol, end='\r', flush=True)
        # Dừng lại 0.1 giây
        time.sleep(0.2)
