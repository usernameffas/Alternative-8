# -------------------------------
# 모듈 임포트 영역
# -------------------------------

import platform   # 운영체제(OS) 및 프로세서(CPU) 등의 기본 시스템 정보를 가져오는 파이썬 표준 라이브러리
import psutil     # 현재 실행 중인 시스템의 자원 사용 현황(CPU, 메모리, 디스크, 네트워크 등)을 조회할 수 있는 강력한 외부 라이브러리
import json       # 파이썬의 dict 자료형을 읽기 좋은 문자열(JSON 포맷)로 변환해주는 모듈

# ----------------------------------------------------------------------------------------
# MissionComputer 클래스 선언
# 시스템 모니터링 기능을 클래스 형태로 객체화하여 재사용성을 높이고, 유지보수가 용이하게 설계
# ----------------------------------------------------------------------------------------
class MissionComputer:
    def __init__(self):
        """
        MissionComputer 클래스의 생성자(Constructor).
        - 여기서는 특별히 초기화할 변수가 없기 때문에 `pass`로 비워 둠.
        - 추후 실제 '임무 컴퓨터' 환경이라면 센서 초기화, 설정값 로드(env_values), 로그 기록 세팅 등을 추가할 수 있음.
        """
        pass

    # ---------------------------
    # 시스템 기본 정보 조회 함수
    # ---------------------------
    def get_mission_computer_info(self):
        """
        미션 컴퓨터의 **정적 시스템 정보**를 조회하는 메서드.
        '정적'이란 프로그램 실행 중에 거의 변하지 않는 정보를 의미한다.
        
        반환 정보 (dict 포맷):
            - 운영체계 (Windows, Linux, Darwin(macOS) 등)
            - 운영체계 버전 (Windows 10의 빌드 넘버, 리눅스 커널 버전 등)
            - CPU 타입 (Intel64 Family, ARM, AMD64 등)
            - CPU 물리적 코어 개수
            - 전체 메모리 크기 (GB 단위, 소수점 둘째 자리까지 반올림)
        """
        try:
            # 시스템 정보 딕셔너리 생성
            info = {
                # platform.system(): 현재 OS 이름(Windows, Linux, Darwin 등)을 반환
                '운영체계': platform.system(),

                # platform.version(): OS의 상세 버전을 문자열로 반환
                '운영체계_버전': platform.version(),

                # platform.processor(): CPU 아키텍처나 모델명 반환 (환경에 따라 비어있을 수도 있음)
                'CPU_타입': platform.processor(),

                # psutil.cpu_count(logical=False): 물리 CPU 코어 수 반환
                # logical=True 하면 하이퍼스레드까지 포함한 논리 코어 수 출력
                'CPU_코어_수': psutil.cpu_count(logical=False),

                # psutil.virtual_memory().total: 전체 메모리 크기(바이트 단위)
                # (1024 ** 3)으로 나누면 GB 단위로 변환됨
                # round(..., 2)는 소수점 둘째 자리까지 반올림
                '메모리_크기_GB': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }

            # dict → JSON 텍스트 변환
            # indent=4 : 들여쓰기 4칸으로 예쁘게 보여주기
            # ensure_ascii=False : 한글이 유니코드 \u 형태 깨지지 않도록 원래 글자로 출력
            print(json.dumps(info, indent=4, ensure_ascii=False))

            # 'info' 딕셔너리를 반환 → 함수 외부에서도 활용 가능
            return info

        except Exception as e:
            # 예외 처리: 만약 psutil 동작 불가, 정보 접근 권한 문제 발생 시
            print(f"시스템 정보 조회 에러: {e}")
            return None

    # ---------------------------
    # 시스템 부하 상태 조회 함수
    # ---------------------------
    def get_mission_computer_load(self):
        """
        미션 컴퓨터의 **동적 상태(부하 상태)**를 조회하는 메서드.
        '동적'이란 시간이 지남에 따라 실시간으로 변하는 CPU/메모리 사용량을 의미한다.
        
        반환 정보 (dict 포맷):
            - CPU 실시간 사용률 (%)
            - 메모리 실시간 사용률 (%)
        """
        try:
            # psutil.cpu_percent(interval=1):
            # 1초 동안 CPU 상태를 샘플링하여 평균 사용률(%) 반환
            # interval을 주지 않으면 직전 호출 이후 사용률이라 정확하지 않을 수 있음
            cpu_usage = psutil.cpu_percent(interval=1)

            # psutil.virtual_memory().percent:
            # 현재 메모리 사용량(%) 반환 (ex: 전체 16GB 중 8GB 사용 → 50%)
            memory_usage = psutil.virtual_memory().percent

            # 결과 값을 딕셔너리에 저장
            load = {
                'CPU_실시간_사용량_%': cpu_usage,
                '메모리_실시간_사용량_%': memory_usage
            }

            # JSON 포맷으로 출력
            print(json.dumps(load, indent=4, ensure_ascii=False))

            # 외부에서 활용 가능하도록 딕셔너리 반환
            return load

        except Exception as e:
            # 예외 처리: psutil 관련 함수 호출 실패 시
            print(f"시스템 부하 조회 에러: {e}")
            return None


# ----------------------------------------------------------------------------------------
# 프로그램 실행 시작점 (엔트리 포인트)
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    파이썬 스크립트의 진입점.
    - 현재 파일을 직접 실행하면 아래 코드 실행
    - 다른 모듈에서 import할 때는 실행되지 않음
    """

    # MissionComputer 클래스의 객체 생성
    runComputer = MissionComputer()

    # 1. 정적 시스템 정보 조회 출력
    print('--- 미션 컴퓨터 시스템 정보 ---')
    runComputer.get_mission_computer_info()

    # 2. 동적 부하 상태(리소스 사용량) 조회 출력
    print('--- 미션 컴퓨터 부하 상태 ---')
    runComputer.get_mission_computer_load()

'''get_mission_computer_info() → 정적 정보 조회

PC의 운영체제(OS), 버전, CPU 종류, 코어 개수, 총 메모리 크기를 확인.

처음 프로그램 시작 시 자기 환경 정보를 출력할 때 유용.

get_mission_computer_load() → 동적 부하 상태 조회

현재 시점의 CPU 사용률(%), **메모리 사용률(%)**을 보여줌.

interval=1 옵션으로 CPU 사용률을 1초 관찰 후 평균치를 가져옴.

출력 형식

둘 다 print(json.dumps(...)) 로 사람이 보기 좋게 JSON(들여쓰기된 구조) 표시.

동시에 함수 리턴값으로도 반환하므로, 파일로 저장하거나 네트워크 전송도 가능.

기타 추가 가능 모듈. ..디스크 사용량 (psutil.disk_usage('/'))

네트워크 송수신량 (psutil.net_io_counters())

GPU 사용률 (NVIDIA GPU면 nvidia-smi 연동)



platform 모듈

정적 정보(운영체제, CPU 종류) 확인 용도.

OS 마다 출력값 형식이 달라질 수 있음.

예: Windows → "Windows", Linux → "Linux", Mac → "Darwin".

psutil 모듈

CPU, 메모리, 디스크, 네트워크, 프로세스 관리까지 가능.

여기서는 CPU 사용량(%), 메모리 총 용량/점유율을 가져오는 데 사용.

실시간 모니터링 툴에 가장 많이 쓰임 (top/htop 프로그램 비슷한 구현 가능).

json.dumps()

dict 자료형 → 사람이 읽기 좋은 문자열(JSON 포맷)로 변환.

ensure_ascii=False로 설정하여 한글 출력 깨짐 방지.

indent=4로 들여쓰기해서 가독성 개선.

클래스 구조의 의미

MissionComputer 클래스 = 실제 "임무 수행용 PC"를 추상화한 객체.

정적 정보(get_mission_computer_info)와 동적 정보(get_mission_computer_load)를 나눠 관리.

나중에 확장할 때(ex. 디스크, 네트워크) 새로운 메소드만 추가하면 됨 (유지보수 ↑'''
