def get_frame_number(filename):
    cap = cv2.VideoCapture(filename)
    frame_no = 0
    while (cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            frame_no += 1
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    return frame_no

def get_image_from_fn(filename, frame_num):
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    count = 0
    while success and count <= frame_num:
        success, image = vidcap.read()
        count += 1

    cv2.imwrite('frametemp.jpg', image)
    vidcap.release()

def check_if_grayscale(filename):
    img = Image.open(str(filename))
    extrema = img.convert("L").getextrema()
    print(extrema)
    if extrema[0] > 230 and extrema[1] > 230:
        return True
    elif extrema[0] < 20 and extrema[1] < 20:
        return True
    else:
        return False