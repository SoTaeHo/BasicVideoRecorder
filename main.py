import cv2
import os

# 현재 스크립트 파일이 있는 디렉토리 얻기
current_directory = os.path.dirname(os.path.abspath(__file__))

# 카메라 영상을 얻기 위한 VideoCapture 객체 생성
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 나타냄, 여러분이 사용하는 웹캠의 인덱스에 따라 변경 가능

# 동영상 파일을 저장할 VideoWriter 객체 생성
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_filename = os.path.join(current_directory, 'output.avi')
out = None

# 블러 필터 활성화 여부를 나타내는 변수
blur_filter_active = False

# 녹화 중인지 여부를 나타내는 변수
recording = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("비디오 캡처 실패.")
        break

    # 녹화 중일 때 왼쪽 상단에 빨간원 생성
    if recording:
        # cv2.circle(frame, (50, 50), 20, (0, 0, 255), -1)  # 빨간색 원
        cv2.putText(frame, "BasicVideoRecorder(recording)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "BasicVideoRecorder", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # 블러 필터 활성화 상태일 때 블러 처리
    if blur_filter_active:
        frame = cv2.blur(frame, (15, 15))  # 블러 처리

    # 프레임을 출력
    cv2.imshow('frame', frame)

    # Record 모드일 때 동영상 파일에 프레임 저장
    if recording:
        if out is None:
            out = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
        out.write(frame)

    # 키 입력 처리
    key = cv2.waitKey(1)
    if key == ord('b'):  # 'b' 키를 누르면 블러 필터 활성화/비활성화 전환
        blur_filter_active = not blur_filter_active
    elif key == ord(' '):  # 'Space' 키를 누르면 녹화 시작 또는 종료
        if not recording:
            recording = True
        else:
            recording = False
            if out is not None:
                out.release()
                out = None
    elif key == 27:  # ESC 키를 누르면 프로그램 종료
        break

# 모든 객체 해제
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
