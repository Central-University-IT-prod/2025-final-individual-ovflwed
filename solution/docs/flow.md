## Работа с приложением

### Flow 1 создание клиентов:

Для создания клиента просто необходимо отправить POST-запрос на /clients/bulk, с данными клиента в теле запроса.
Пример запроса:
```json
[
    {
        "age": 0,
        "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "gender": "MALE",
        "location": "string",
        "login": "string"
    }
]
```

Удостоверимся, что клиент создался: получим его через GET-запрос на /clients/{client_id}
```json
{
    "age": 0,
    "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "gender": "MALE",
    "location": "string",
    "login": "string"
}
```
аналогично, можно обновить данные клиента.

### Flow 2 создание кампаний:
Для создания кампании просто необходимо отправить POST-запрос на /advertisers/bulk, с данными кампании в теле запроса.
Пример запроса:
```json
[
    {
        "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string"
    }
]
```

Удостоверимся, что кампания создалась: получим ее через GET-запрос на /advertisers/{advertiser_id}
```json
{
    "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "string"
}
```
аналогично, можно обновить данные кампании.

### Flow 3 управление рекламными объявлениями:

Для создания объявления просто необходимо отправить POST-запрос на /advertisers/{advertiser_id}/campaigns, с данными объявления в теле запроса.
Пример запроса:
```json
{
  "ad_text": "string",
  "ad_title": "string",
  "clicks_limit": 0,
  "cost_per_click": 0,
  "cost_per_impression": 0,
  "end_date": 0,
  "impressions_limit": 0,
  "start_date": 0,
  "targeting": {
    "age_from": 0,
    "age_to": 0,
    "gender": "MALE",
    "location": "string"
  }
}
```

Удостоверимся, что объявление создалось: получим его через GET-запрос на /advertisers/{advertiser_id}/campaigns/{campaign_id}
```json
{
  "ad_text": "string",
  "ad_title": "string",
  "clicks_limit": 0,
  "cost_per_click": 0,
  "cost_per_impression": 0,
  "end_date": 0,
  "impressions_limit": 0,
  "start_date": 0,
  "targeting": {
    "age_from": 0,
    "age_to": 0,
    "gender": "MALE",
    "location": "string"
  },
  "image_url": null,
}
```

Заметим поле image_url. Это поле будет содержать ссылку на картинку, которая будет отображаться в объявлении. Добавить картинку можно через POST-запрос на /advertisers/{advertiser_id}/campaigns/{campaign_id}/image указав в параметре file form-data картинку в формате jpeg. После загрузки снова получим кампанию через GET-запрос на /advertisers/{advertiser_id}/campaigns/{campaign_id}

image_url = "http://localhost/ad-images/.....jpg" - ссылка на картинку в хранилище, через реверс-прокси

если необходимо удалить картинку, то можно отправить DELETE-запрос на /advertisers/{advertiser_id}/campaigns/{campaign_id}/image,
аналогично, можно удалить объявление через DELETE-запрос на /advertisers/{advertiser_id}/campaigns/{campaign_id}

Для получения всех объявлений стоит использовать GET-запрос на /advertisers/{advertiser_id}/campaigns предоствляющий пагинированый список объявлений.
По умолчанию возвращается первые 10 объявлений, можно изменить количество через параметры size и page.
```json
    [
        {...}, // ad1
        {...}, // ad2
        ...
    ]
```
Обновить объявление можно через PUT-запрос на /advertisers/{advertiser_id}/campaigns/{campaign_id}, со всеми полями объявления в теле запроса, включая image_url.

### Flow 4 управление скорами
Для управления скорами необходимо отправить POST-запрос на /ml-scores, с данными скора в теле запроса.
Пример запроса:
```json
{
  "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "score": 0
}
```
Тогда скор будет обновлен или создан, в зависимости от переданных значений.

### Flow 5 работа с рекламой
Для получения объявлений, которые подходят для клиента, необходимо отправить GET-запрос на /ads с параметром client_id.
Пример ответа:
```json
{
  "ad_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "ad_text": "string",
  "ad_title": "string",
  "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "image_url": "http://glo.api/images/mr-good.png"
}
```

Для фиксации клика на объявление необходимо отправить POST-запрос на /ads/{ad_id}/clicks с client_id в теле запроса.
пример запроса:
```json
{
  "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

## Flow 6 статистика

Для получения статистики по кампании необходимо отправить GET-запрос на /stats/campaigns/{campaign_id}, в ответе будет статистика по кампании за все время.

Пример ответа:
```json
{
  "clicks_count": 0,
  "conversion": 0,
  "impressions_count": 0,
  "spent_clicks": 0,
  "spent_impressions": 0,
  "spent_total": 0
}
```

Аналогично для сводной статистики по рекламодателю.
GET /stats/advertisers/{advertiser_id}/campaigns вернет:

```json 
{
  "clicks_count": 0,
  "conversion": 0,
  "impressions_count": 0,
  "spent_clicks": 0,
  "spent_impressions": 0,
  "spent_total": 0
}
```

Для получения статистики по кампании за каждый день необходимо отправить GET-запрос на /stats/campaigns/{campaign_id}/daily в ответе будет список словарей вида:
```json
[
  {
    "clicks_count": 0,
    "conversion": 0,
    "impressions_count": 0,
    "spent_clicks": 0,
    "spent_impressions": 0,
    "spent_total": 0,
    "date": 0
  },
  {
    "clicks_count": 0,
    "conversion": 0,
    "impressions_count": 0,
    "spent_clicks": 0,
    "spent_impressions": 0,
    "spent_total": 0,
    "date": 1
  }
]
```
Аналогично для сводной статистики по рекламодателю: /stats/advertisers/{advertiser_id}/daily

Flow 7 графическая статистика
Для того чтобы увидеть дэшборд необходимо зайти на {host}:3000, войдя в Grafana под стандартным логином и паролем (admin/admin), открыть вкладку dashboards -> Prod -> Сервис рекламы.

![Папка с дэшбордами](../images/dashboards.png)

Пример: ![Grafana](../images/dashboard.png)