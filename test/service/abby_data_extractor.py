from service.AbbyyOnlineSdk import AbbyyOnlineSdk, ProcessingSettings
#from AbbyyOnlineSdk import AbbyyOnlineSdk, ProcessingSettings
import time
import pandas as pd
#from docx import Document
from os import path


def create_processor():
    processor = AbbyyOnlineSdk()
    processor.ApplicationId = "Pdfocrpoc003" #"mrngstar"
    processor.Password = "gaV+iLuqfBUluWun0TCo1sxA" #"OU0Eixew9trPorzq5Kmn/yQx"

    return processor


def extract_to_docx(page_pdf_path, docx_output_path):
    processor = create_processor()

    print("Uploading..")
    settings = ProcessingSettings()
    settings.Language = "English"
    #settings.OutputFormat = "docx"
    settings.OutputFormat = "txt"
    task = processor.process_image(page_pdf_path, settings)
    if task is None:
        print("Error")
        return
    if task.Status == "NotEnoughCredits":
        print("Not enough credits to process the document. Please add more pages to your application's account.")
        return

    print("Id = {}".format(task.Id))
    print("Status = {}".format(task.Status))

    # Wait for the task to be completed
    print("Waiting..")
    # Note: it's recommended that your application waits at least 2 seconds
    # before making the first getTaskStatus request and also between such requests
    # for the same task. Making requests more often will not improve your
    # application performance.
    # Note: if your application queues several files and waits for them
    # it's recommended that you use listFinishedTasks instead (which is described
    # at http://ocrsdk.com/documentation/apireference/listFinishedTasks/).

    while task.is_active():
        time.sleep(5)
        print(".", end="")
        task = processor.get_task_status(task)

    print("Status = {}".format(task.Status))

    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            processor.download_result(task, docx_output_path)
            print("Result was written to {}".format(docx_output_path))
    else:
        print("Error processing task")

    return docx_output_path


def get_tables_from_pdf(pdf_path):
    docx_output_path = path.join(path.dirname(pdf_path), f"{path.splitext(path.basename(pdf_path))[0]}.docx")
    extract_to_docx(pdf_path, docx_output_path)

    return extract_tables_from_docx(docx_output_path)


#pdf_path = "/Users/shravanc/flask/aditya_birla/test_files/Ketul/uploads/uploads/essar/pdfs/stitched.pdf"
#output_path = "/Users/shravanc/flask/aditya_birla/test_files/Ketul/uploads/uploads/essar/pdfs/output.txt"

#pdf_path = "/Users/shravanc/flask/aditya_birla/test_files/Ketul/uploads/uploads/chandrasheel/pdfs/stitched.pdf"
#output_path = "/Users/shravanc/flask/aditya_birla/test_files/Ketul/uploads/uploads/chandrasheel/pdfs/output.txt"
#pdf_path = "/Users/shravanc/flask/aditya_birla/ocr-pdf-aditya-malaysia/uploads/ketul/pages/stitched.pdf"
#output_path = "/Users/shravanc/flask/aditya_birla/ocr-pdf-aditya-malaysia/uploads/ketul/pages/output.txt"
#extract_to_docx(pdf_path, output_path)


