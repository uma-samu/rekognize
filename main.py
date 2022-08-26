import requests
import os
import base64
from jproperties import Properties

vision_api_url_template = "https://vision.googleapis.com/v1/images:annotate?key={}"
headers = {"content-type": "application/json", "accept": "application/json"}
path_of_the_input_directory = 'input'
path_of_the_output_directory = 'output'
ext = '.jpeg'
configs = Properties()


def detect_image_and_annotate(file_name):
    print("Calling API to detect image and annotate")

    # reading from the input file
    input_file_path = '{}/{}'.format(path_of_the_input_directory, file_name)
    with open(input_file_path, 'rb') as image_file:
        content_value = base64.b64encode(image_file.read()).decode("utf-8")

    # calling the visions api and detecting the image
    payload = """{"requests":[{"image": {"content": "%s"},"features": [{"type": "TEXT_DETECTION"}]}]}""" % content_value
    response = requests.post(vision_api_url_template.format(configs.get('api_key').data), payload, headers=headers)
    print("Response is " + str(response.status_code))
    response_json = response.json()
    text_detected = response_json['responses'][0]['fullTextAnnotation']['text']

    # writing to the output file
    output_file_path = '{}/{}.txt'.format(path_of_the_output_directory, os.path.splitext(file_name)[0])
    print("Writing output to file ... "+output_file_path)
    with open(output_file_path, 'w') as f:
        f.write(text_detected)


if __name__ == '__main__':
    # read properties
    with open('application.properties', 'rb') as config_file:
        configs.load(config_file)

    # for every file in input directory, process the file
    for input_file in os.listdir(path_of_the_input_directory):
        if input_file.endswith(ext):
            print("#########################################")
            print("Processing file ... " + input_file)
            detect_image_and_annotate(input_file)
        else:
            continue
