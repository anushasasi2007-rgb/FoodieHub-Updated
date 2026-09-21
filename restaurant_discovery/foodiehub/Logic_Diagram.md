```mermaid
flowchart TD
    A[Start FoodieHub] --> B[Login / Create Account]
    B --> C{Account Valid?}
    C -->|No| D[Show Error]
    D --> B
    C -->|Yes| E[Home Page]
    E --> F[View Restaurants]
    E --> G[Search Restaurants]
    E --> H[Write Review]
    E --> I[View Profile]
    G --> J[Search by Name / Location / Cuisine]
    H --> K[Select Restaurant]
    K --> L[Give Rating and Review]
    L --> M[Save Review in Database]
    M --> E