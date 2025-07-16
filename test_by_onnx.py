import onnxruntime as ort
import time, os, cv2,argparse
import numpy as np
pic_form = ['.jpeg','.jpg','.png','.JPEG','.JPG','.PNG']
from glob import glob

def parse_args():
    desc = "Tensorflow implementation of AnimeGANv3"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-i', '--input_imgs_dir', type=str, default='/home/ada/test_data', help='video file or number for webcam')
    parser.add_argument('-m', '--model_path', type=str, default='models/AnimeGANv3_Hayao_36.onnx',  help='file path to save the modles')
    parser.add_argument('-o', '--output_path', type=str, default='./output/' ,help='output path')
    parser.add_argument('-d','--device', type=str, default='cpu', choices=["cpu","gpu"] ,help='running device')
    return parser.parse_args()

def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def process_image(img, model_name):
    h, w = img.shape[:2]
    # resize image to multiple of 8s
    def to_8s(x):
        # If using the tiny model, the multiple should be 16 instead of 8.
        if 'tiny' in os.path.basename(model_name) :
            return 256 if x < 256 else x - x % 16
        else:
            return 256 if x < 256 else x - x % 8
    img = cv2.resize(img, (to_8s(w), to_8s(h)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)/ 127.5 - 1.0
    return img

def load_test_data(image_path, model_name):
    img0 = cv2.imread(image_path).astype(np.float32)
    img = process_image(img0, model_name)
    img = np.expand_dims(img, axis=0)
    return img, img0.shape

def save_images(images, image_path, size):
    images = (np.squeeze(images) + 1.) / 2 * 255
    images = np.clip(images, 0, 255).astype(np.uint8)
    images = cv2.resize(images, size)
    cv2.imwrite(image_path, cv2.cvtColor(images, cv2.COLOR_RGB2BGR))

def Convert(input_img_path, output_path, onnx="model.onnx", device="cpu"):
    """Process a single image file"""
    if not os.path.exists(input_img_path):
        raise FileNotFoundError(f"Input file does not exist: {input_img_path}")

    if os.path.splitext(input_img_path)[-1] not in pic_form:
        raise ValueError("Unsupported image format")

    os.makedirs(output_path, exist_ok=True)

    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if ort.get_device() == 'GPU' and device == "gpu" else ['CPUExecutionProvider']
    session = ort.InferenceSession(onnx, providers=providers)

    x_name = session.get_inputs()[0].name
    y_name = session.get_outputs()[0].name

    start = time.time()
    sample_image, shape = load_test_data(input_img_path, onnx)
    fake_img = session.run(None, {x_name: sample_image})
    
    output_img_path = os.path.join(output_path, os.path.basename(input_img_path))
    save_images(fake_img[0], output_img_path, (shape[1], shape[0]))

    print(f"Processed {input_img_path} in {time.time() - start:.3f}s")