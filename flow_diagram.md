# Semantic Search Microservice - Flow Diagram

## Application Startup Flow
```
┌─────────────────┐
│   App Startup   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Load Retriever  │
│ from pickle     │
│ (artifacts/     │
│  retriever.pkl) │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Initialize      │
│ FastAPI App     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Server Ready    │
│ (Listening)     │
└─────────────────┘
```

## Request Processing Flow
```
┌─────────────────┐
│ Client Request  │
│ POST /sematic   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ FastAPI Router  │
│ Receives Query  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Input Validation│
│ • Parse JSON    │
│ • Check text    │
│ • Strip spaces  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐      ┌─────────────────┐
│ Text Empty?     │ YES  │ Return HTTP 400 │
│                 ├─────►│ Error Response  │
└─────────┬───────┘      └─────────────────┘
          │ NO
          ▼
┌─────────────────┐
│ Create Search   │
│ Instance        │
│ • query=text    │
│ • retriever=pkl │
└─────────┬───────┘
          │
          ▼
┌───────────────── ┐
│ Execute Semantic │
│ Search           │
│                  |
|sematic_results() │
└─────────┬─────── ┘
          │
          ▼
┌─────────────────┐
│ Create Response │
│ QueryResponse   │
│ (results=result)│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Format Results  │
│ • Enumerate     │
│ • Extract       │
│   page_content  │
│ • Join with \n\n│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Return Formatted│
│ String Response │
└─────────────────┘
```

## Home Page Flow
```
┌─────────────────┐
│ Client Request  │
│ GET /           │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐      ┌─────────────────┐
│ Check if        │ YES  │ Return HTML     │
│ static/index.   ├─────►│ File Content    │
│ html exists     │      └─────────────────┘
└─────────┬───────┘
          │ NO
          ▼
┌─────────────────┐
│ Return Default  │
│ HTML Response   │
│ <h1>Sematic     │
│ Search...</h1>  │
└─────────────────┘
```

## Data Flow Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───►│  FastAPI App    │───►│   Search Class  │
│   (Text Input)  │    │  (Validation)   │    │  (Processing)   │
└─────────────────┘    └─────────────────┘    └─────────┬───────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Formatted       │◄───│ QueryResponse   │◄───│   Retriever     │
│ String Results  │    │   (Model)       │    │ (Pre-trained)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```