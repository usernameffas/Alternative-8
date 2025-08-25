import platform
import psutil
import json

class MissionComputer:
    def __init__(self):
        # 기존 env_values 및 Sensor 초기화 등 필요시 추가 가능
        pass

    def get_mission_computer_info(self):
        """
        미션 컴퓨터의 시스템 정보를 조회하여 JSON 형태로 출력하는 메소드
        """
        try:
            info = {
                '운영체계': platform.system(),
                '운영체계_버전': platform.version(),
                'CPU_타입': platform.processor(),
                'CPU_코어_수': psutil.cpu_count(logical=False),
                '메모리_크기_GB': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }
            print(json.dumps(info, indent=4, ensure_ascii=False))
            return info
        except Exception as e:
            print(f"시스템 정보 조회 에러: {e}")
            return None

    def get_mission_computer_load(self):
        """
        미션 컴퓨터의 CPU, 메모리 부하 상태를 조회하여 JSON 형태로 출력하는 메소드
        """
        try:
            load = {
                'CPU_실시간_사용량_%': psutil.cpu_percent(interval=1),
                '메모리_실시간_사용량_%': psutil.virtual_memory().percent
            }
            print(json.dumps(load, indent=4, ensure_ascii=False))
            return load
        except Exception as e:
            print(f"시스템 부하 조회 에러: {e}")
            return None


if __name__ == '__main__':
    runComputer = MissionComputer()
    print('--- 미션 컴퓨터 시스템 정보 ---')
    runComputer.get_mission_computer_info()
    print('--- 미션 컴퓨터 부하 상태 ---')
    runComputer.get_mission_computer_load()
