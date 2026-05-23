"""
Гіпотеза Колатца — паралельні обчислення
=========================================
Для кожного числа від 1 до N обчислюється кількість кроків
для виродження в 1 (послідовність Колатца).
Використовується ThreadPool для паралельного виконання.
"""

import time
from multiprocessing.pool import ThreadPool
import os

# ── Параметри (перевизначаються через змінні середовища Docker) ────────────
N           = int(os.environ.get("COLLATZ_N", 10_000_000))
NUM_THREADS = int(os.environ.get("COLLATZ_THREADS", os.cpu_count() or 4))
# ───────────────────────────────────────────────────────────────────────────


def collatz_steps(n: int) -> int:
    """Повертає кількість кроків для виродження числа n у 1."""
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def compute_chunk(args):
    """Обчислює кроки для діапазону [start, end). Повертає список кроків."""
    start, end = args
    return [collatz_steps(num) for num in range(start, end)]


def main():
    print("╔══════════════════════════════════════════════╗")
    print("║     Гіпотеза Колатца — паралельні обчислення  ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"  Числа  : 1 … {N:,}")
    print(f"  Потоки : {NUM_THREADS}")
    print()

    chunk_size = N // NUM_THREADS
    chunks = [
        (i * chunk_size + 1,
         (i + 1) * chunk_size + 1 if i < NUM_THREADS - 1 else N + 1)
        for i in range(NUM_THREADS)
    ]

    print("  Запуск обчислень...")
    t_start = time.perf_counter()

    all_steps = []
    with ThreadPool(processes=NUM_THREADS) as pool:
        for partial in pool.imap_unordered(compute_chunk, chunks):
            all_steps.extend(partial)

    elapsed   = time.perf_counter() - t_start
    max_steps = max(all_steps)
    max_num   = all_steps.index(max_steps) + 1

    print()
    print("  ✔ Обчислення завершено!")
    print("  ─────────────────────────────────────────────")
    print(f"  Загальний час        : {elapsed:.4f} с")
    print(f"  Середня к-сть кроків : {sum(all_steps) / N:.4f}")
    print(f"  Макс. кроків         : {max_steps}  (число {max_num:,})")
    print(f"  Мін. кроків          : {min(all_steps)}  (число 1)")
    print("  ─────────────────────────────────────────────")
    print()

    print("  Перші 10 чисел — кроки до 1:")
    for i in range(10):
        print(f"    {i+1:>3} → {all_steps[i]} кроків")


if __name__ == "__main__":
    main()
