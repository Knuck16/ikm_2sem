import random


class Barge:
    def __init__(self, num_holds, max_barrels):

    def _validate_hold(self, hold_num):
        if not 1 <= hold_num < len(self._holds):
            self._error = True
            self._error_message = f"ОШИБКА: Неверный номер отсека {hold_num}"
            return False
        return True

        if self._current > self._limit:
            self._error = True
            self._error_message = f"ОШИБКА: Превышен лимит {self._limit} бочек"
            return False

            return True

    def remove_barrel(self, hold_num, expected_fuel):

            return False

            actual_fuel = self._holds[hold_num].pop()
            if actual_fuel != expected_fuel:

            self._current -= 1
            return True

    def is_empty(self):

    def get_state(self):
        state = []
        for i, hold in enumerate(self._holds[1:], 1):
            state.append(f"Отсек {i}: {hold}")
        state.append(f"Текущее количество: {self._current}")
        state.append(f"Максимальное количество: {self._max}")
        state.append(f"Ошибка: {self._error_message if self._error else 'нет'}")
        return "\n".join(state)

    def get_result(self):
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

        operations.append((op, hold, fuel))
    return operations

def simulate():
    while True:
        try:
                continue
            break
        except ValueError:
            print("Ошибка: введите целые числа!")

    while True:
        mode = input("\nВыберите режим:\n1 - Автоматическая генерация операций\n2 - Ручной ввод операций\n> ").strip()
        if mode in ('1', '2'):
            break
        print("Ошибка: введите 1 или 2")


    barge = Barge(K, P)
    print("\nНачальное состояние:")
    print(barge.get_state())


        print(barge.get_state())

        if not success:
            break

    if not barge._error and not barge.is_empty():
        barge._error = True
        barge._error_message = "ОШИБКА: Баржа не пуста в конце"
        print(f"\n! Обнаружена ошибка: {barge._error_message}")

    print(barge.get_result())


if __name__ == "__main__":
    simulate()