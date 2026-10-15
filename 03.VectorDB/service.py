'''
    This block create a vector database
    For this example we are gooing with Qdrant

    Workflow
        - create_database -> chunking -> document_loader
        : Document loader load  documents present in our storage.
        : Which is passed to chunking where recursive text splitter create chunks for embedding model.
        : Embedding model create vectors and store them in our vector database.

    NOTE: It will be a batch serivce which runs on a defined schedule to add new documents from blob storage to our vectordb.
    Later this DB is used by our RAG Engine to retrieve information to answer user queries.

'''


import Qdrant
import OpenAIEmbeddings

embedding = OpenAIEmbeddings(
    model=os.environ.get("EMBEDDING_MODEL").
    show_progress=True
)


def document_loader(): 
    '''
        Loading all documents from our Blob storage to add them to our knowledge base(vector DB).
    '''
    dir_loader = DirectoryLoader(
        path=temp_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = dir_loader.load()

    return docs

def chunking():
    '''
        Creating chunks for embedding model for database creation and updation.
    '''
    docs = document_loader()
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )

    chunks = splitter.split_documents(docs)
    return chunks

def create_database():
    '''
        CREATING DATABASE FOR THE FIRST TIME
    '''
    docs = chunking()
    client = Quadrant.connect()
    database = client.from_documents(
        docs,
        embedding=embeddings,
        collection_name="myvectorstore"
    )

def update_database():
    '''
        UPDATE DATABASE LOGIC HERE BASED ON REQUIREMENTS
    '''
    pass

if database:
    update_database()
else:
    create_database()
