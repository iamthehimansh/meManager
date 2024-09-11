import csv
import requests
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.schema import Document
import logging
logging.basicConfig(level=logging.INFO)
# logging in a file
logging.basicConfig(filename='log.log', level=logging.INFO)
CHROMA_PATH = "../data/chroma"

def read_jobs_csv():
    job_csv=open('../data/jobs.csv', 'r')
    logging.info("Reading jobs.csv")
    return job_csv.read()
def write_jobs_csv(position, status, salary, location, company, description):
    job_csv=open('../data/jobs.csv', 'a')
    writer = csv.writer(job_csv)
    writer.writerow([position, status, salary, location, company, description])
    job_csv.close()
    write_to_vector_db(f"position: {position}, status: {status}, salary: {salary}, location: {location}, company: {company}, description: {description}")
    logging.info("Job added successfully")
    logging.info(f"position: {position}, status: {status}, salary: {salary}, location: {location}, company: {company}, description: {description}")
    return "Job added successfully"
def notify_user(message, title, email_subject, impotant_link=""):
    notification_csv=open('../data/notifications.csv', 'a')
    writer = csv.writer(notification_csv)
    writer.writerow([message, title, email_subject, impotant_link])
    notification_csv.close()
    # TODO: Notify the user
    logging.info("User notified successfully")
    logging.info(f"message: {message}, title: {title}, email_subject: {email_subject}, impotant_link: {impotant_link}")
    return "User notified successfully"
def unsubscribe_mail(why, unsubscribe_url, email):
    unsubscribe_csv=open('../data/unsubscribes.csv', 'a')
    writer = csv.writer(unsubscribe_csv)
    writer.writerow([why, unsubscribe_url, email])
    unsubscribe_csv.close()
    requests.get(unsubscribe_url)
    return "User unsubscribed successfully"
def search_from_vector_db(query_text):
    
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function= OllamaEmbeddings(model="mxbai-embed-large"))
    try:
        # Search the DB.
        results = db.similarity_search_with_relevance_scores(query_text, k=6)
        
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        refrence_text = []
        for doc, _score in results:
            refrence_text.append(doc.metadata)
        print(refrence_text)
        return context_text+"\n\n---\n\nRefrence To all above one by one: "+"\n".join(refrence_text)
    except:
        return "No data found/error occured in the vector database"
def write_to_vector_db(textToAdd):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function= OllamaEmbeddings(model="mxbai-embed-large"))
    doc = Document(page_content=textToAdd)
    db.add_documents(doc)
    # db.persist()
    
    return "Data added to vector database"