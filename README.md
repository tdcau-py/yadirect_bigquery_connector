Структура:
1.	Необходима выгрузка по всем аккаунтам доступных на данном агентском логине со следующими данными:
•	Название аккаунта
•	Количество показов
•	Количество кликов
•	CTR
•	Количество конверсии
•	Цена конверсии
•	Расход по аккаунту
•	Остаточный баланс аккаунта на текущий момент если возможно


2.	Возможность выгрузка всех аккаунтов с подробной статистикой по рекламным кампаниям со следующими данными:
•	Название рекламной кампании
•	Количество показов
•	Количество кликов
•	CTR
•	Количество конверсии
•	Цена конверсии
•	Расход по рекламной кампании
Для всех перечисленных выгрузок необходима возможность указывать период выгружаемых данных, для аккаунта возможность выбора целей (может быть не одна, несколько) при этом в разных аккаунтах может быть разный набор целей. Выбор модели атрибуции для всех аккаунтов одна. Также необходима возможность указать другой токен.
При загрузке новых данных по ранее уже выгруженному аккаунту данные должны перезаписываться.
Данные выгружать в BigQuery для работы Looker Studio. 
Если возможно, то хочется это реализовать через GUI, в которой можно установить даты выгрузок, прописать цели для каждого аккаунта и модель атрибуции и токен
Если нет возможности сделать в GUI, то через питон с инструкцией.
