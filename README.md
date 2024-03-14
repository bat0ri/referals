# RESTful API сервис для реферальной системы.

## Запуск
перейти в директорию ```src/```
``` Linux
docker-compose --file docker-compose-local.yaml up -d  
```
- Swagger запущен ```http://127.0.0.1:8000/docs#/```
- Redoc ```http://127.0.0.1:8000/redoc```


## Функциональные требования:
- регистрация и аутентификация пользователя (JWT);
- аутентифицированный пользователь может обновить код (создать новый активный --> старый станет инактив). Одновременно может быть активен только 1 код. При создании кода задан его срок годности равный 2 минутам;
- возможность получения реферального кода по email адресу реферера;
- возможность регистрации по реферальному коду в качестве реферала;	
- получение информации о рефералах по id реферера;
- UI документация (Swagger/ReDoc).



## Модели
**User** - Пользователь
| Атрибут       | Описание                                         |
|---------------|--------------------------------------------------|
| id            | Уникальный идентификатор пользователя.           |
| email         | Электронная почта пользователя.                  |
| hash_password | Хэшированный пароль пользователя.                |
| create_date   | Дата и время создания пользователя.              |

**ReferalCode** - Реферальный код
| Атрибут    | Описание                                        |
|------------|-------------------------------------------------|
| id         | Уникальный идентификатор реферального кода.     |
| code       | Реферальный код.                                |
| parent_id  | Идентификатор пользователя, которому принадлежит реферальный код(реферер). |
| exp_date   | Срок годности реферального кода.                |
| is_active  | Флаг активности реферального кода.              |

**Referalship** - Отношение код-реферал
| Атрибут    | Описание                                        |
|------------|-------------------------------------------------|
| id         | Уникальный идентификатор связи реферального кода с пользователем. |
| code_id    | Идентификатор реферального кода.                |
| user_id    | Идентификатор реферала.                     |

### Отношения таблиц
- **User к ReferalCode**: Каждый пользователь может иметь много реферальных кодов, но каждый реферальный код принадлежит только одному пользователю.
- **ReferalCode к Referalship**: Каждый реферальный код может быть использован многократно, но каждая запись в Referalship связана только с одним реферальным кодом.

