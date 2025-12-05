import purchase_analyzer

def main():
    input_file = "purchases.txt"  # файл с данными
    output_file = "report.txt"    # файл для отчёта
    
    print("анализируем файл purchases.txt...")
  
    purchases = purchase_analyzer.read_purchases(input_file)
    print(f"найдено валидных покупок: {len(purchases)}")
    
    errors = purchase_analyzer.count_errors(input_file)
    print(f"найдено строк с ошибками: {errors}")
    
    total = purchase_analyzer.total_spent(purchases)
    print(f"общая сумма покупок: {total:.2f}")
    
    print("\nтраты по категориям:")
    categories = purchase_analyzer.spent_by_category(purchases)
    for cat in sorted(categories.keys()):
        print(f"  {cat}: {categories[cat]:.2f}")
    
    print("\nтоп-3 самых дорогих покупок:")
    top3 = purchase_analyzer.top_n_expensive(purchases, 3)
    for i, item in enumerate(top3, 1):
        print(f"  {i}. {item['name']}: {item['total']:.2f}")
    
    purchase_analyzer.write_report(purchases, errors, output_file)
    print(f"\nотчёт сохранён в файл {output_file}")

# запускаем программу, только если файл запущен напрямую
if __name__ == "__main__":
    main()
