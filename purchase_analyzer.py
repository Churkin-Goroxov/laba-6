def read_purchases(path):
    """
    читает файл и возвращает список покупок
    каждая покупка - словарь с полями: date, category, name, price, qty, total
    невалидные строки пропускаются
    """
    purchases = []
    
    with open(path, 'r') as file:
        for line in file:
            # убираем пробелы и пропускаем пустые строки
            line = line.strip()
            if not line:
                continue
            
            # делим строку на части
            parts = line.split(';')
            
            # проверяем, что частей ровно 5
            if len(parts) != 5:
                continue
            
            # убираем пробелы в каждой части
            date, category, name, price_str, qty_str = [p.strip() for p in parts]
            
            # проверяем, что обязательные поля не пустые
            if not (date and category and name):
                continue
            
            # пробуем преобразовать цену и количество в числа
            try:
                price = float(price_str)
                qty = float(qty_str)
            except ValueError:
                # если не получилось - строка невалидна
                continue
            
            # проверяем, что цена и количество положительные
            if price <= 0 or qty <= 0:
                continue
            
            # добавляем валидную покупку в список
            purchases.append({
                'date': date,
                'category': category,
                'name': name,
                'price': price,
                'qty': qty,
                'total': price * qty
            })
    
    return purchases


def count_errors(path):
    """
    считает количество невалидных строк в файле
    """
    valid_count = 0
    total_count = 0
    
    with open(path, 'r') as file:
        for line in file:
            # считаем все непустые строки
            if line.strip():
                total_count += 1
    
    # считаем валидные строки через уже готовую функцию
    valid_count = len(read_purchases(path))
    
    # ошибки=все строки-валидные строки
    return total_count - valid_count


def total_spent(purchases):
    """
    считает общую сумму всех покупок
    """
    total = 0
    for purchase in purchases:
        total += purchase['total']
    return total


def spent_by_category(purchases):
    """
    считает сумму покупок по каждой категории
    возвращает словарь: категория -> сумма
    """
    result = {}
    
    for purchase in purchases:
        category = purchase['category']
        cost = purchase['total']
        
        # если категории ещё нет в словаре - создаём
        if category not in result:
            result[category] = 0
        
        # добавляем стоимость покупки к категории
        result[category] += cost
    
    return result


def top_n_expensive(purchases, n=3):
    """
    возвращает n самых дорогих покупок
    """
    # сортируем покупки по общей стоимости (от большей к меньшей)
    sorted_purchases = sorted(purchases, key=lambda p: p['total'], reverse=True)
    
    return sorted_purchases[:n]


def write_report(purchases, errors, out_path):
    """
    создаёт текстовый отчёт с анализом покупок
    """
    with open(out_path, 'w') as file:
      
        file.write("отчёт по покупкам\n")
        file.write("=" * 40 + "\n\n")
        
        # основная статистика
        file.write(f"валидных покупок: {len(purchases)}\n")
        file.write(f"строк с ошибками: {errors}\n")
        file.write(f"общая сумма: {total_spent(purchases)}\n\n")
        
        # траты по категориям
        file.write("траты по категориям:\n")
        file.write("-" * 30 + "\n")
        
        categories = spent_by_category(purchases)
        for cat in sorted(categories.keys()):
            file.write(f"{cat} {categories[cat]}\n")
        
        file.write("\n")
        
        # топ-3 покупки
        file.write("топ-3 самых дорогих покупок:\n")
        file.write("-" * 40 + "\n")
        
        top3 = top_n_expensive(purchases, 3)
        for i, purchase in enumerate(top3, 1):
            file.write(f"{i}. {purchase['name']} ")
            file.write(f"{purchase['total']} ({purchase['category']})\n")
        
        # подробный список всех покупок
        if purchases:
            file.write("\n" + "=" * 40 + "\n")
            file.write("все валидные покупки:\n")
            file.write("=" * 40 + "\n")
            
            for purchase in purchases:
                file.write(f"{purchase['date']} | {purchase['category']} | ")
                file.write(f"{purchase['name']} | ")
                file.write(f"{purchase['price']} x {purchase['qty']} = ")
                file.write(f"{purchase['total']}\n")
