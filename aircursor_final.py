import cv2
import mediapipe as mp
import pyautogui
import time
import math

# Setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot access camera.")
    exit()

hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

smoothening = 7
prev_x, prev_y = 0, 0
last_action = 0
cooldown = 1.5  # seconds

click_down = False
right_click_down = False

# Helper function to calculate distance between two points
def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

print("✅ AirCursor started. Press ESC to exit.")

# Create a window and move it to bottom-right corner
cv2.namedWindow("AirCursor", cv2.WINDOW_NORMAL)
cv2.resizeWindow("AirCursor", 300, 220)
cv2.moveWindow("AirCursor", screen_w - 320, screen_h - 280)
cv2.setWindowProperty("AirCursor", cv2.WND_PROP_TOPMOST, 1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    h, w, _ = frame.shape

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        lm = hand.landmark

        # Get coordinates
        ix, iy = int(lm[8].x * w), int(lm[8].y * h)       # Index
        mx, my = int(lm[12].x * w), int(lm[12].y * h)     # Middle
        rx, ry = int(lm[16].x * w), int(lm[16].y * h)     # Ring
        px, py = int(lm[20].x * w), int(lm[20].y * h)     # Pinky
        tx, ty = int(lm[4].x * w), int(lm[4].y * h)       # Thumb
        wrist_y = int(lm[0].y * h)                        # Palm

        # Cursor Movement (index finger)
        move_x = screen_w / w * ix
        move_y = screen_h / h * iy
        curr_x = prev_x + (move_x - prev_x) / smoothening
        curr_y = prev_y + (move_y - prev_y) / smoothening
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        now = time.time()

        # ✋ Clicks using pinch gestures
        index_thumb_dist = distance(ix, iy, tx, ty)
        middle_thumb_dist = distance(mx, my, tx, ty)

        # Left Click: Index + Thumb pinch
        if index_thumb_dist < 40:
            if not click_down:
                click_down = True
                pyautogui.click()
        else:
            click_down = False

        # Right Click: Middle + Thumb pinch
        if middle_thumb_dist < 40:
            if not right_click_down:
                right_click_down = True
                pyautogui.rightClick()
        else:
            right_click_down = False

        # 🖱️ Scroll Up (Index + Middle up)
        if iy < h * 0.4 and my < h * 0.4 and abs(ix - mx) < 40:
            pyautogui.scroll(10)

        # 🖱️ Scroll Down (Index + Middle down)
        if iy > h * 0.6 and my > h * 0.6 and abs(ix - mx) < 40:
            pyautogui.scroll(-10)

        # ➡️ Next: Only middle finger up
        if (
            my < wrist_y and
            iy > wrist_y and ry > wrist_y and py > wrist_y and ty > wrist_y
        ):
            if now - last_action > cooldown:
                print("➡️ Next Slide")
                pyautogui.press('right')
                last_action = now

        # ⬅️ Previous: Middle + Ring + Pinky up
        if (
            my < wrist_y and ry < wrist_y and py < wrist_y and
            iy > wrist_y and ty > wrist_y
        ):
            if now - last_action > cooldown:
                print("⬅️ Previous Slide")
                pyautogui.press('left')
                last_action = now

    # 📷 Show webcam preview in bottom-right corner
    preview = cv2.resize(frame, (640, 480))
    cv2.imshow("AirCursor", preview)

    # 🛑 Exit with ESC
    if cv2.waitKey(1) == 27:
        print("🛑 Exiting AirCursor.")
        break

cap.release()
cv2.destroyAllWindows()
