# ⚡ Key Counter

실시간 키 연타 횟수 측정 및 기록 프로그램

![Key Counter 스크린샷](/key_counter.png)

## 주요 기능

- **정확한 연타 측정**: 키를 누르고 뗄 때마다 1회씩 카운트
- **실시간 기록**: DOWN/UP 이벤트를 ms 단위로 기록
- **간격 표시**: 각 이벤트 간 시간 차이 자동 계산
- **전역 후킹**: 다른 프로그램 실행 중에도 백그라운드 작동

## 설치

### 필수 요구사항
- Python 3.7 이상

### 라이브러리 설치

```bash
pip install pynput
```

> **주의**: `keyboard` 라이브러리가 설치되어 있다면 충돌 방지를 위해 제거하세요
> ```bash
> pip uninstall keyboard
> ```

## 사용법

### 1. 프로그램 실행

```bash
python key_counter_with_record.py
```

관리자 권한으로 실행해야 다른 프로그램에서도 키 입력을 감지할 수 있습니다.

### 2. 키 선택
- "키를 선택하려면 클릭하세요" 버튼 클릭
- 측정할 키를 한 번 누름 (예: Space, A, Ctrl 등)

### 3. 측정 시작
- **▶ 시작** 버튼 클릭
- 선택한 키를 연타하면 실시간으로 기록됨

### 4. 기록 확인
기록 테이블에서 다음 정보를 확인할 수 있습니다:
- **키**: 누른 키 이름
- **이벤트**: DOWN (누름) / UP (뗌)
- **경과시간**: 첫 입력부터 현재까지 시간 (ms)
- **간격**: 이전 이벤트와의 시간 차이 (ms)

### 5. 정지 및 초기화
- **⏸ 정지**: 측정 일시 정지
- **초기화**: 카운트와 기록 모두 삭제

## 활용 사례
- **게임**: 연타 속도 측정 및 분석
- **타이핑 연습**: 특정 키 입력 빈도 확인
- **성능 테스트**: 키보드 응답 시간 분석

## 문제 해결

### 키 입력이 감지되지 않음
→ 프로그램을 **관리자 권한**으로 실행하세요

**Windows**:
```bash
# 관리자 권한 명령 프롬프트에서 실행
python key_counter_with_record.py
```

**macOS/Linux**:
```bash
sudo python3 key_counter_with_record.py
```

### AttributeError: 'keyboard' 관련 오류
→ 다른 keyboard 라이브러리와 충돌
```bash
pip uninstall keyboard
pip install pynput
```

## 기술 스택
- Python 3.7+
- tkinter (GUI)
- pynput (전역 키보드 후킹)
- ttk.Treeview (테이블 뷰)

## 개인정보 보호
- 다른 키 입력이나 텍스트는 수집하지 않음
- 모든 데이터는 로컬에서만 처리
- 네트워크 연결 불필요

