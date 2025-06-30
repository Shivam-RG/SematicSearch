# Semantic Search Microservice - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEMANTIC SEARCH MICROSERVICE                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   Client/UI     │    │   FastAPI App   │    │   Storage    │ │
│  │                 │    │                 │    │              │ │
│  │ • Web Browser   │◄──►│ • REST API      │◄──►│ • retriever  │ │
│  │ • HTTP Client   │    │ • Route Handler │    │   .pkl       │ │
│  │ • Frontend      │    │ • Validation    │    │ • Artifacts  │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│                                   │                             │
│                                   ▼                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                 CORE COMPONENTS                            │ │
│  │                                                            │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │ │
│  │  │   Models    │    │   Search    │    │   Retriever     │ │ │
│  │  │             │    │   Engine    │    │                 │ │ │
│  │  │ • Query     │    │             │    │                 │ │ │
│  │  │ • Response  │    │ • Semantic  │    │ • Vector Store  │ │ │
│  │  │ • Validation│    │   Search    │    │ • Embeddings    │ │ │
│  │  └─────────────┘    └─────────────┘    └─────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        TECHNOLOGY STACK                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Web Framework:     FastAPI                                     │
│  Language:          Python                                      │
│  Serialization:     Pickle                                      │
│  Data Models:       Pydantic                                    │
│  HTTP Protocol:     REST API                                    │
│  Response Format:   JSON                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
