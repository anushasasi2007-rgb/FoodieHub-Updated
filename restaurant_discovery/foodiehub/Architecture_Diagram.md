```mermaid
flowchart TD
    A[User] --> B[Streamlit Frontend]

    B --> C[Login / Register]
    B --> D[Restaurant Discovery]
    B --> E[Search & Filter]
    B --> F[Reviews & Ratings]
    B --> G[User Profile]

    C --> H[Python Backend]
    D --> H
    E --> H
    F --> H
    G --> H

    H --> I[(SQLite Database)]

    I --> J[Users Table]
    I --> K[Restaurants Table]
    I --> L[Reviews Table]
