import random


class Barge:
    def __init__(self, num_holds, max_barrels):
        self._holds = [[] for _ in range(num_holds + 1)]  # Отсеки (индексация с 1)
        self._current = 0  # Текущее количество бочек
        self._max = 0  # Максимальное количество бочек
        self._limit = max_barrels  # Лимит бочек
        self._error = False  # Флаг ошибки
        self._error_message = ""  # Сообщение об ошибке

    def _validate_hold(self, hold_num):
        """Проверка номера отсека"""
        if not 1 <= hold_num < len(self._holds):
            self._error = True
            self._error_message = f"ОШИБКА: Неверный номер отсека {hold_num}"
            return False
        return True

    def add_barrel(self, hold_num, fuel_type):
        """Добавление бочки в отсек"""
        if self._error: return False

        if not self._validate_hold(hold_num): return False

        self._holds[hold_num].append(fuel_type)
        self._current += 1

        if self._current > self._max:
            self._max = self._current

        if self._current > self._limit:
            self._error = True
            self._error_message = f"ОШИБКА: Превышен лимит {self._limit} бочек"
            return False

        return True

    def remove_barrel(self, hold_num, expected_fuel):
        """Извлечение бочки из отсека"""
        if self._error: return False

        if not self._validate_hold(hold_num): return False

        if not self._holds[hold_num]:
            self._error = True
            self._error_message = f"ОШИБКА: Отсек {hold_num} пуст"
            return False

        actual_fuel = self._holds[hold_num].pop()
        if actual_fuel != expected_fuel:
            self._error = True
            self._error_message = f"ОШИБКА: Ожидалось {expected_fuel}, а получили {actual_fuel}"
            return False

        self._current -= 1
        return True

    def is_empty(self):
        """Проверка, пуста ли баржа"""
        if self._error: return False
        return all(not hold for hold in self._holds)

    def get_state(self):
        """Возвращает строку с текущим состоянием"""
        state = []
        for i, hold in enumerate(self._holds[1:], 1):
            state.append(f"Отсек {i}: {hold}")
        state.append(f"Текущее количество: {self._current}")
        state.append(f"Максимальное количество: {self._max}")
        state.append(f"Ошибка: {self._error_message if self._error else 'нет'}")
        return "\n".join(state)

    def get_result(self):
        """Финальный результат"""
        if not self.is_empty() and not self._error:
            self._error = True
            self._error_message = "ОШИБКА: Баржа не пуста в конце"
        return self._max if not self._error else "Error"


def generate_operations(N, K):
    """Генерация случайных операций"""
    operations = []
    hold_states = [[] for _ in range(K + 1)]

    print("\nСгенерированные операции:")
    for _ in range(N):
        available = [i for i in range(1, K + 1) if hold_states[i]]

        if available and random.random() < 0.5:
            hold = random.choice(available)
            fuel = hold_states[hold][-1]
            operations.append(('-', hold, fuel))
            print(f"- {hold} {fuel} (выгружаем {fuel} из отсека {hold})")
            hold_states[hold].pop()
        else:
            hold = random.randint(1, K)
            fuel = random.randint(1, 10000)
            operations.append(('+', hold, fuel))
            print(f"+ {hold} {fuel} (добавляем {fuel} в отсек {hold})")
            hold_states[hold].append(fuel)

    return operations


def manual_input_operations(N, K):
    """Ручной ввод операций"""
    operations = []
    print("\nВводите операции в формате: [+/-] [номер_отсека] [тип_топлива]")
    print("Например: + 1 5000 (добавить бочку 5000 в отсек 1)")
    print("Или: - 2 3000 (удалить бочку 3000 из отсека 2)\n")

    for i in range(1, N + 1):
        while True:
            op_str = input(f"Операция {i}/{N}: ").strip()
            parts = op_str.split()
            if len(parts) != 3:
                print("Ошибка: введите 3 значения через пробел!")
                continue

            op, hold_str, fuel_str = parts
            if op not in ('+', '-'):
                print("Ошибка: операция должна быть + или -!")
                continue

            try:
                hold = int(hold_str)
                fuel = int(fuel_str)
                if not 1 <= hold <= K:
                    print(f"Ошибка: номер отсека должен быть от 1 до {K}!")
                    continue
                break
            except ValueError:
                print("Ошибка: номер отсека и тип топлива должны быть числами!")

        operations.append((op, hold, fuel))
    return operations

def simulate():
    """Симуляция с подробными логами"""
    # Ввод параметров
    while True:
        try:
            K = int(input("Введите количество отсеков (K): "))
            P = int(input("Введите лимит бочек (P): "))
            N = int(input("Введите количество операций (N): "))
            if K <= 0 or P <= 0 or N <= 0:
                print("Ошибка: значения должны быть положительными!")
                continue
            break
        except ValueError:
            print("Ошибка: введите целые числа!")

    # Выбор режима
    while True:
        mode = input("\nВыберите режим:\n1 - Автоматическая генерация операций\n2 - Ручной ввод операций\n> ").strip()
        if mode in ('1', '2'):
            break
        print("Ошибка: введите 1 или 2")

    if mode == '1':
        operations = generate_operations(N, K)
    else:
        operations = manual_input_operations(N, K)

    # Создание баржи
    barge = Barge(K, P)
    print("\nНачальное состояние:")
    print(barge.get_state())

    # Обработка операций
    for i, op in enumerate(operations, 1):
        print(f"\nШаг {i}: Операция {op[0]} {op[1]} {op[2]}")

        if op[0] == '+':
            success = barge.add_barrel(op[1], op[2])
        else:
            success = barge.remove_barrel(op[1], op[2])

        print(barge.get_state())

        if not success:
            print(f"! Произошла ошибка: {barge._error_message}")
            break

    # Финальная проверка
    if not barge._error and not barge.is_empty():
        barge._error = True
        barge._error_message = "ОШИБКА: Баржа не пуста в конце"
        print(f"\n! Обнаружена ошибка: {barge._error_message}")

    # Результат
    print("\nФинальный результат:")
    print(barge.get_result())


if __name__ == "__main__":
    simulate()