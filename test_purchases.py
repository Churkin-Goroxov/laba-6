import purchase_analyzer
import os

def test_simple():
    """тест на простых данных"""
    # создаём временный файл
    with open("test_simple.txt", "w") as f:
        f.write("2025-01-01;food;apple;10.0;2\n")
        f.write("2025-01-02;food;banana;5.0;3\n")
    
    try:
        # тестируем чтение
        purchases = purchase_analyzer.read_purchases("test_simple.txt")
        assert len(purchases) == 2, "должно быть 2 покупки"
        
        # тестируем общую сумму
        total = purchase_analyzer.total_spent(purchases)
        assert total == 35.0, f"ожидалось 35.0, получено {total}"
        
        # тестируем категории
        categories = purchase_analyzer.spent_by_category(purchases)
        assert "food" in categories, "должна быть категория food"
        assert categories["food"] == 35.0, f"ожидалось 35.0, получено {categories['food']}"
        
        print("✓ test_simple пройден")
    finally:
        # удаляем временный файл
        if os.path.exists("test_simple.txt"):
            os.remove("test_simple.txt")

def test_errors():
    """тест на обработку ошибок"""
    # создаём файл с ошибками
    with open("test_errors.txt", "w") as f:
        f.write("2025-01-01;food;apple;10.0;2\n")      # валидная
        f.write("2025-01-02;food;banana;abc;3\n")      # ошибка: цена не число
        f.write("\n")                                  # пустая строка
        f.write("2025-01-03;food;orange;5.0;xyz\n")   # ошибка: количество не число
        f.write("2025-01-04;food;grape;-5.0;2\n")     # ошибка: отрицательная цена
    
    try:
        # тестируем чтение (должна быть только 1 валидная)
        purchases = purchase_analyzer.read_purchases("test_errors.txt")
        assert len(purchases) == 1, f"должна быть 1 покупка, а не {len(purchases)}"
        
        # тестируем подсчёт ошибок
        errors = purchase_analyzer.count_errors("test_errors.txt")
        # всего непустых строк: 4, валидных: 1, ошибок: 3
        assert errors == 3, f"ожидалось 3 ошибки, получено {errors}"
        
        print(" test_errors пройден")
    finally:
        # удаляем временный файл
        if os.path.exists("test_errors.txt"):
            os.remove("test_errors.txt")

def test_top_n():
    """тест поиска самых дорогих покупок"""
    # создаём тестовые данные
    purchases = [
        {"name": "чай", "price": 2.0, "qty": 1, "total": 2.0},
        {"name": "кофе", "price": 5.0, "qty": 2, "total": 10.0},
        {"name": "молоко", "price": 3.0, "qty": 2, "total": 6.0},
        {"name": "вода", "price": 1.0, "qty": 1, "total": 1.0},
    ]
    
    # тестируем топ-2
    top2 = purchase_analyzer.top_n_expensive(purchases, 2)
    assert len(top2) == 2, "должно быть 2 покупки"
    assert top2[0]["name"] == "кофе", "первая должна быть кофе"
    assert top2[1]["name"] == "молоко", "вторая должна быть молоко"
    
    # тестируем топ-10 (больше, чем есть)
    top10 = purchase_analyzer.top_n_expensive(purchases, 10)
    assert len(top10) == 4, "должно быть 4 покупки"
    
    print("✓ test_top_n пройден")

def test_empty():
    """тест пустого файла"""
    with open("test_empty.txt", "w") as f:
        pass  # пустой файл
    
    try:
        purchases = purchase_analyzer.read_purchases("test_empty.txt")
        assert len(purchases) == 0, "не должно быть покупок"
        
        errors = purchase_analyzer.count_errors("test_empty.txt")
        assert errors == 0, "не должно быть ошибок"
        
        total = purchase_analyzer.total_spent(purchases)
        assert total == 0, "сумма должна быть 0"
        
        categories = purchase_analyzer.spent_by_category(purchases)
        assert len(categories) == 0, "не должно быть категорий"
        
        print(" test_empty пройден")
    finally:
        if os.path.exists("test_empty.txt"):
            os.remove("test_empty.txt")

def test_whitespace():
    """тест обработки пробелов"""
    with open("test_ws.txt", "w") as f:
        f.write("  2025-01-01  ;  food  ;  apple  ;  10.0  ;  2  \n")
        f.write("2025-01-02;food;banana;5.0;3\n")
    
    try:
        purchases = purchase_analyzer.read_purchases("test_ws.txt")
        assert len(purchases) == 2, "должно быть 2 покупки"
        
        # проверяем, что пробелы убраны
        assert purchases[0]["date"] == "2025-01-01"
        assert purchases[0]["category"] == "food"
        assert purchases[0]["name"] == "apple"
        
        print("test_whitespace пройден")
    finally:
        if os.path.exists("test_ws.txt"):
            os.remove("test_ws.txt")

def test_write_report():
    """тест создания отчёта"""
    purchases = [
        {
            "date": "2025-01-01",
            "category": "food",
            "name": "apple",
            "price": 10.0,
            "qty": 2,
            "total": 20.0
        },
        {
            "date": "2025-01-02", 
            "category": "transport",
            "name": "bus",
            "price": 5.0,
            "qty": 1,
            "total": 5.0
        }
    ]
    
    # создаём отчёт
    purchase_analyzer.write_report(purchases, 3, "test_report.txt")
    
    try:
        # проверяем, что файл создан
        assert os.path.exists("test_report.txt"), "файл отчёта должен быть создан"
        
        # читаем содержимое
        with open("test_report.txt", "r") as f:
            content = f.read()
        
        # проверяем ключевые фразы в отчёте
        assert "отчёт по покупкам" in content
        assert "валидных покупок: 2" in content
        assert "строк с ошибками: 3" in content
        assert "общая сумма: 25.00" in content
        assert "food" in content
        assert "transport" in content
        
        print("test_write_report пройден")
    finally:
        if os.path.exists("test_report.txt"):
            os.remove("test_report.txt")

# запускаем все тесты
if __name__ == "__main__":
    print("запускаем тесты...\n")
    
    test_simple()
    test_errors()
    test_top_n()
    test_empty()
    test_whitespace()
    test_write_report()
    
    print("\nвсе тесты пройдены успешно!")
