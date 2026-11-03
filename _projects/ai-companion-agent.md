---
layout: project
title: AI 컴패니언 Agent
subtitle: 캐릭터 페르소나, 장기기억, 선제적 대화와 Tool 활용을 결합한 개인 AI 컴패니언
description: 캐릭터 페르소나, 장기기억, 선제적 대화와 Tool 활용을 결합한 개인 AI 컴패니언
tags: [Generative Agent, Agentic Workflow, Google ADK, Long-term Memory, Knowledge Graph, MCP, Agent as Tool, Proactive Agent, Hybrid Decision, ComfyUI]
demo:
  type: prototype
  src: /demos/ai-companion-agent/
  height: 700
---

## Overview

캐릭터 페르소나 기반 대화에 장기기억과 Tool 활용을 결합한 개인 비서 Agent입니다. 대화에서 얻은 정보를 Knowledge Graph에 축적하고, 캐릭터의 감정·행동·장소를 유지해 응답과 선제적 대화에 반영합니다.

Planner가 필요한 정보를 판단해 기억 검색, 웹 검색, 메모 관리와 Codex/Claude CLI 작업 위임을 수행합니다. [투자 비서 Agent](../investment-agent/)·[포트폴리오 Agent](../portfolio-agent/)를 MCP로 연동하고, 가상 세계의 상태와 ComfyUI 이미지 생성을 대화에 연결했습니다.

## Demo

<div id="demo-slot"></div>

## Key Features

### 1. 근거를 보존하는 장기기억
- 대화에서 기억할 사실을 비동기로 추출하고, 기존 엔티티를 식별·연결해 Neo4j에 저장합니다.
- 벡터·전문 검색을 RRF로 결합해 요약 기억과 원본 근거를 검색합니다. 최근 대화 문맥을 함께 활용해 생략된 주제도 찾도록 구성했습니다.
- 일일 회고(Reflection)로 누적된 사실을 요약 기억으로 정리합니다. 원본 근거를 연결하고 사실 요약과 캐릭터의 주관적 회고를 구분합니다.
- 현실·가상 경험의 범위와 출처를 함께 보존하여, 가상 세계의 사건을 사용자의 현실 행동으로 혼동하지 않도록 합니다.

### 2. 계획 판단과 도구 실행
- 기억 검색 후 Planner가 답변 생성 또는 추가 Tool 호출을 선택합니다. 실행 결과를 받아 다시 판단하는 루프를 일반 대화와 선제적 대화가 공유합니다.
- 도구는 기억 검색, 웹 검색, 사용자 메모 저장·조회·수정, CLI 작업 위임으로 구성합니다. 메모의 사용자 수정과 AI 제안을 분리합니다.
- 시간이 걸리는 전문 리서치·경력 분석은 백그라운드 작업으로 실행하고, 대화를 계속할 수 있도록 완료 후 결과를 별도로 전달합니다.
- 도구 인자를 스키마로 검증하고, 호출 횟수·전체 시간·문맥 크기를 제한합니다. 같은 턴의 동일 호출은 이전 결과를 재사용합니다.

### 3. 선제적 대화와 영속적인 가상 세계
- 최근 대화·기억과 캐릭터 상태를 바탕으로 먼저 말을 걸지 판단합니다. 응답에서 미래 알림 약속을 추출해 리마인더로 저장합니다.
- 가상 세계에서 캐릭터의 행동·장소·의상을 주기적으로 갱신하고, 그 변화를 대화의 계기로 활용합니다.
- 사용자의 가상 세계 참여 여부와 캐릭터와의 위치 관계를 관리해, 현재 상황에 맞는 대화와 이미지 생성에 활용합니다.
- 생성 도중 대화나 상황이 바뀌면 전송 전에 재검증합니다. 웹·Telegram 간 알림 전달과 메시지 미러링을 지원합니다.

### 4. 경량 판단 모델을 활용한 LLM 효율화
- 경량 판단 모델(Jev)이 변경·추출 필요 여부 등을 먼저 판단하고, 복잡한 판단은 LLM으로 넘기는 게이트·캐스케이드 구조를 구현했습니다.
- 판단 단계별로 LLM 단독·섀도 평가·캐스케이드를 선택할 수 있습니다. Tool 인자 생성처럼 복잡한 계획은 LLM이 담당합니다.
- 섀도 모드는 실제 LLM 결과를 유지하면서 Jev와의 일치 여부를 기록합니다. 운영 중 표본 비교와 실패 시 폴백을 지원합니다.
- 비교 일치율은 두 모델의 판단 차이를 확인하는 지표이며, 정답률이나 비용 절감률과 구분합니다.

### 5. 이미지 공유와 멀티 채널 인터페이스
- 대화 모델이 응답에서 이미지 공유를 결정하면, 텍스트 전달 후 ComfyUI로 해당 장면을 비동기 생성합니다.
- 장면 설명을 태그형 프롬프트로 바꾸고 의상·장소와 결합합니다. Character LoRA와 얼굴·손 디테일러를 적용합니다.
- 이미지 생성 중 대화·캐릭터 상태가 바뀌었는지 전달 전에 확인하고, 결과를 대화 이력과 갤러리에 저장합니다.
- 웹(Live2D), Telegram, Tauri 데스크탑·Android 앱이 하나의 대화 세션을 공유하며 응답을 스트리밍합니다.

## Architecture

```mermaid
flowchart LR
  CH["웹 · 데스크탑 · Android · Telegram"] --> CORE["FastAPI 코어"]
  CORE --> RECALL["기억 검색"]
  RECALL --> PLAN["계획 판단"]
  PLAN -->|도구 필요| TOOL["검증된 도구 실행"]
  TOOL --> PLAN
  PLAN -->|답변 가능| DECIDE["상태·리마인더 판단"]
  DECIDE --> TEXT["응답 스트리밍"]
  TOOL --> EXT["웹 검색 · 메모 · CLI 위임"]
  TOOL --> JOB["전문 리서치·경력 분석 접수"]
  JOB -. 완료 후 별도 전달 .-> CORE
  WORLD["가상 세계 · 선제대화 · 리마인더"] --> RECALL
  DECIDE -. 일부 판단 .-> JEV["경량 판단 모델"]
  TEXT -. 전달 후 .-> POST["기억 기록 · 상태 갱신 · 약속 추출"]
  TEXT -. 모습·사진 행동 .-> IMG["ComfyUI 이미지 생성"]
  POST --> NEO[("Neo4j 기억")]
  POST --> PG[("PostgreSQL 대화·상태")]
  RECALL --> NEO
  REFLECT["일일 회고"] --> NEO
  NEO --> REFLECT
```

## Challenges

### 대화가 길어져도 이전 경험을 기억하는 방법

대화 기록을 모두 전달하는 대신, 중요한 사실을 장기기억으로 저장하고 관련된 내용만 검색하도록 구성했습니다. 누적된 기억은 주기적으로 요약하되 원본 근거를 연결해, 요약과 실제 대화 내용을 함께 확인할 수 있게 했습니다.

### 먼저 말을 걸어도 현재 대화의 흐름을 놓치지 않도록

AI가 먼저 보낼 메시지나 이미지를 만드는 동안 사용자가 새로 말하거나 상황이 바뀔 수 있습니다. 결과를 보내기 직전에 현재 대화와 상황을 다시 확인해, 이미 지나간 맥락에 대한 응답을 제어했습니다.

### 모든 판단에 큰 LLM을 호출해야 할까?

기억 저장이나 상태 변경이 필요한지 같은 단순 판단에 경량 모델을 적용했습니다. 기존 LLM과 결과를 비교하는 섀도 평가를 두고, 신뢰도가 낮거나 처리가 어려운 경우 LLM으로 넘기도록 설계했습니다.

## Tech Stack

| 영역 | 기술 |
|---|---|
| AI | Google ADK, Gemini·OpenRouter, Jev, ComfyUI·LoRA |
| Backend | Python, FastAPI, Tavily, Codex/Claude CLI, MCP |
| Data | Neo4j, PostgreSQL |
| Client | TypeScript·Vite·PixiJS(Live2D), Tauri, Android, Telegram Bot |
