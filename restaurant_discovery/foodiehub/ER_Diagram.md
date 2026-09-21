```mermaid
erDiagram

    USERS {
        int id PK
        string username
        string password
    }

    RESTAURANTS {
        int id PK
        string name
        string location
        string cuisine
        string price
        float rating
    }

    REVIEWS {
        int id PK
        int user_id FK
        int restaurant_id FK
        int rating
        string review
    }

    USERS ||--o{ REVIEWS : writes
    RESTAURANTS ||--o{ REVIEWS : receives