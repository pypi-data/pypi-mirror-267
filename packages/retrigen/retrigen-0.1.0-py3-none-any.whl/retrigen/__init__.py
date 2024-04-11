from typing import List, Dict, Union, Tuple
import textdescriptives as td  # noqa
import spacy
import uuid
from langchain_core.documents import Document
from tqdm import tqdm
import json
import logging
from typing import Dict, Any
from tqdm import tqdm
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions


def filter_text_by_td(text_list: List[Union[str, Document]], filter_type: bool = True) -> List[Document]:
    """
    Filter documents by the textdescriptives quality check, converts strings to langchain Docs

    Args:
        text_list: A list of text strings or Document objects.
        filter_type: A boolean defining whether to filter by texts that passed (True) or failed (False) the textdescriptives quality check.

    Returns:
        A list of Document objects that passed the textdescriptives quality check.
    """
    nlp = spacy.blank("da")  # Assuming 'da' is the desired model
    nlp.add_pipe("sentencizer")
    quality_pipe = nlp.add_pipe("textdescriptives/quality")

    # Process the texts with SpaCy, handling both strings and Document objects
    processed_docs = list(nlp.pipe(doc.page_content if isinstance(doc, Document) else doc for doc in text_list))

    # Filter based on the quality check, merge with existing metadata
    filtered_docs = [
        Document(page_content=doc.text, metadata=getattr(original_doc, "metadata", {}))
        for original_doc, doc in zip(text_list, processed_docs)
        if doc._.passed_quality_check == filter_type
    ]

    return filtered_docs


def q_eval_system_prompt():
    sys_prompt = """Din opgave er at evaluere et givet tekstuddrag for at bestemme, om det er egnet til at danne grundlag for et generelt spørgsmål, der er relevant for eksempelvis en eksamen eller en test. 
    For at vurdere dette, skal du fokusere på følgende tre nøglekriterier:

    1. Klarhed: Vurder, om teksten er formuleret klart og direkte, således at et spørgsmål til denne tekst, vil kunne besvares uden yderligere forklaringer. Teksten skal være læsbar og ikke usammenhængende i sin struktur.
    
    2. Konkret Information: Afgør, om uddraget indeholder specifikke, faktuelle informationer, der kan danne grundlag for et præcist og direkte spørgsmål. Teksten skal præsentere håndgribelige fakta eller data, som et spørgsmål kan baseres på.

    3. Kontekstuel Helhed: Bedøm, om teksten leverer tilstrækkelig kontekst for at et spørgsmål baseret på uddraget vil være meningsfuldt og forståeligt uden behov for yderligere information. Teksten skal være selvstændig og give en fuld forståelse af det emne, der behandles.

    Baseret på din evaluering:

    - Tildel scoren 1, hvis tekstuddraget opfylder alle tre kriterier, og der kan formuleres et naturligt, klart og kontekstuelt meningsfuldt spørgsmål baseret på teksten.

    - Tildel scoren 0, hvis tekstuddraget ikke opfylder et eller flere af de ovenstående kriterier, hvilket gør det uegnet til at danne grundlag for et generelt spørgsmål.
    """
    return sys_prompt


def q_eval_user_prompt(text: str) -> str:
    """Prepare the prompt for the API call."""

    qa_egnet_tmlp = """Du er en erfaren sagsbehandler. 
    Din Opgave:
    Vurder det følgende tekstuddrag og angiv, om det er egnet til at stille et generelt spørgsmål til.

    Uddrag:
    {chunk_text}
    
    Returner din vurdering i følgende JSON-format:

    {{
    "llm_score": [indsæt enten 0 eller 1 her]
    }}
    """
    return qa_egnet_tmlp.format(chunk_text=text)


def json_api_call(oai_client, system_prompt: str, user_prompt: str, oai_model: str = "gpt-3.5-turbo-0125") -> Dict[str, Any]:
    """Perform the API call to evaluate the text."""
    try:
        completion = oai_client.chat.completions.create(
            model=oai_model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing failed: {e}")
    except Exception as e:
        logging.error(f"API call failed: {e}")
    return {}


def filter_text_by_llm(text_list: List[Union[str, Document]]) -> List[Document]:
    """Filter text chunks by an LLM quality check

    Args:
        text_list: A list of text strings or Document objects.

    Returns:
        A list of Document objects that passed the LLM quality check.
    """

    texts_passed_llm = []
    system_prompt = q_eval_system_prompt()
    oai_client = OpenAI()
    for text_item in tqdm(text_list, desc="Evaluating texts"):
        # Extract text content from Document objects or use string directly
        text_content = text_item.page_content if isinstance(text_item, Document) else text_item

        user_prompt = q_eval_user_prompt(text_content)
        response = json_api_call(oai_client, system_prompt, user_prompt)
        if response:
            if response.get("llm_score") == 1:
                # Preserve original Document object or create a new one if the input was a string
                passed_text_doc = text_item if isinstance(text_item, Document) else Document(page_content=text_content)
                texts_passed_llm.append(passed_text_doc)
            else:
                continue
        else:
            logging.error(f"Failed to evaluate the following text due to an earlier error:\n{text_content}")

    return texts_passed_llm


def generate_question_template(text: str, num_q: int = 1) -> str:
    question_tmlp = """Nedenfor er et uddrag (kontekst) fra en længere tekst:
    ---------------------
    {context_str}
    ---------------------
    Givet ovenstående uddrag og ingen forudgående viden, er din opgave at generere præcis {num_questions_per_chunk} spørgsmål til teksten.
    En sætning skal kun indeholde 1 spørgsmål, og spørgsmålet skal være formuleret kort og præcist. 
    Svaret til spørgsmålet, skal kunne findes i ovenstående uddrag.
    Spørgsmålet skal indeholde specifik kontekst, således at spørgsmålet efterfølgende kan besvares entydigt og uden kendskab til uddraget. 
    Spørgsmålene skal stilles i et sprog som en borger uden juridisk ekspertise kan forstå.

    Eksempel på et spørgsmål der ikke har en specifik kontekst, og som fejlagtigt indeholder 2 spørgsmål i 1 sætning: 
    "Hvilket dokument har den nye vejledning erstattet, og hvornår blev den udsendt?" -Da det ikke angivet hvilket dokument der er tale om, og derfor er svaret til spørgsmålet ikke entyidgt, uden kendskab til uddraget. Sætningen indeholder desuden 2 spørgsmål i samme sætning. 

    Eksempel på et godt spørgsmål, som kan besvares entydigt uden kendskab til uddraget:
    "Hvilke to indbetalinger udgør det samlede medlemsbidrag til en a-kasse?" - Da det er klart hvad der spørges om, og der kun er 1 rigtigt svar i den givne lovtekst.
    """
    return question_tmlp.format(context_str=text, num_questions_per_chunk=num_q)


def question_api_call(oai_client, user_prompt: str, oai_model: str = "gpt-4-0125-preview") -> Dict[str, Any]:
    """Perform the API call to evaluate the text."""
    try:
        completion = oai_client.chat.completions.create(
            model=oai_model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "Din opgave er at stille præcise spørgsmål til et givet tekstuddrag og returnere en JSON med en liste af spørgsmål i formatet {{Q: [spørgsmål1, spørsmål2, ...}}.",
                },
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing failed: {e}")
    except Exception as e:
        logging.error(f"API call failed: {e}")
    return {"Q": "API error"}


class QuestionContextManager:
    """
    Manages a collection of questions and their associated context chunks as Document objects.
    Allows for adding questions with contexts and displaying a specified number of these question-context pairs.
    """

    def __init__(self):
        self.questions: Dict[str, Document] = {}
        self.contexts: Dict[str, Document] = {}
        self.question_context_id_pairs: Dict[str, List[str]] = {}

    def add_question_context(self, question: Document, context: Document):
        """
        Adds a question and its associated context (both as Document objects) to the manager.
        Generates unique IDs for both the question and the context, storing them and their association.

        Parameters:
        - question (Document): The Document object containing the question.
        - context (Document): The Document object containing the context.
        """
        unique_question_id = str(uuid.uuid4())
        unique_context_id = str(uuid.uuid4())
        self.questions[unique_question_id] = question
        self.contexts[unique_context_id] = context
        self.question_context_id_pairs[unique_question_id] = [unique_context_id]

    @property
    def question_context_pairs(self) -> List[Tuple[Document, List[Document]]]:
        """
        Returns a list of tuples, each containing a question Document and a list of its associated context Documents.
        """
        return [(self.questions[qid], [self.contexts[cid] for cid in self.question_context_id_pairs[qid]]) for qid in self.questions]

    def display_question_context_pairs(self, num_pairs: int = None):
        """
        Displays a specified number of question-context pairs. If no number is specified, all pairs are displayed.

        Parameters:
        - num_pairs (int, optional): The number of question-context pairs to display. If None, all pairs are displayed. Defaults to None.
        """
        displayed_pairs = 0
        for q_id, context_ids in self.question_context_id_pairs.items():
            if num_pairs is not None and displayed_pairs >= num_pairs:
                break

            question = self.questions[q_id]
            print(f"Question: {question.page_content}")
            for c_id in context_ids:
                context = self.contexts[c_id]
                print(f"\nContext: {context.page_content}")
            print("-" * 40)  # Separator for readability
            displayed_pairs += 1

    def filter_questions_by_length(self, min_length: int = 20, max_length: int = 150):
        """
        Filters out questions that do not fall within the specified minimum and maximum character length.
        Updates the object by removing questions and their associated contexts that do not meet the criteria.

        Parameters:
        - min_length (int): The minimum character length for questions to be kept. Default to 20.
        - max_length (int): The maximum character length for questions to be kept. Default to 150.
        """
        questions_to_remove = [q_id for q_id, question in self.questions.items() if not (min_length <= len(question.page_content) <= max_length)]

        # Remove the questions and question_context pairs
        for q_id in questions_to_remove:
            del self.questions[q_id]
            del self.question_context_id_pairs[q_id]

        # Identify contexts that are no longer linked to any questions
        contexts_to_remove = {
            context_id for context_id in self.contexts if all(context_id not in contexts for contexts in self.question_context_id_pairs.values())
        }

        # Remove these contexts
        for context_id in contexts_to_remove:
            del self.contexts[context_id]

        print(f"Removed {len(questions_to_remove)} questions.")

    def update_question_context_pairs(self, q_c_to_append: Dict[str, List[str]]):
        """
        Appends the question-context matches to the existing question_context_id_pairs,
        ensuring no duplicates are added.

        Parameters:
        - q_c_to_append (Dict[str, List[str]]): A dictionary with question IDs as keys and lists of context IDs to append as values.
        """
        for q_id, c_id_list in q_c_to_append.items():
            if q_id in self.question_context_id_pairs:
                # Create a set from the existing IDs for quick lookup
                existing_ids_set = set(self.question_context_id_pairs[q_id])
                # Filter out duplicates while preserving order
                filtered_c_id_list = [c_id for c_id in c_id_list if c_id not in existing_ids_set]
                # Extend the existing list with the filtered, non-duplicate IDs
                self.question_context_id_pairs[q_id].extend(filtered_c_id_list)
            else:
                # Directly assign the list if the q_id is not already present
                self.question_context_id_pairs[q_id] = c_id_list

    def __repr__(self):
        return f"<QuestionContextManager with {len(self.questions)} questions>"


def generate_questions(
    textContexts: List[Union[Document, str]], num_questions: int = 1, oai_model: str = "gpt-4-0125-preview", duplicate_metadata: bool = True
) -> QuestionContextManager:
    """
    Generates questions from a list of context Documents and returns a QuestionContextManager
    containing the generated questions and their contexts.

    Parameters:
    - textContexts (List[Union[Document, str]]): A list of Document objects or strings to generate questions from.
    - num_questions (int): Number of questions to generate per context. Default is 1.
    - oai_model (str): The model to use for generating questions. Default is "gpt-4-0125-preview".
    - duplicate_metadata (bool): If True, duplicate the metadata from context to the generated questions.

    Returns:
    QuestionContextManager: An object containing the generated questions and their contexts.
    """
    oai_client = OpenAI()
    result = QuestionContextManager()
    for context in tqdm(textContexts):
        # If input is simply a list of strings, convert to doc with empty metadata
        if isinstance(context, str):
            context = Document(page_content=context, metadata={})

        question_prompt = generate_question_template(context.page_content, num_questions)
        response = question_api_call(oai_client, question_prompt, oai_model)
        try:
            questions = response["Q"]
            for question_text in questions:
                question_document = Document(page_content=question_text.strip(), metadata=context.metadata if duplicate_metadata else {})
                result.add_question_context(question_document, context)
        except KeyError as e:
            print(f"Error parsing json response: {e}")
    return result


def initialize_chroma_collection(
    client: chromadb.Client, collection_name: str, embedding_model: str, similarity_metric: str = "cosine"
) -> chromadb.Collection:
    """Initialize or reset a ChromaDB collection with a specified embedding model.

    Args:
        client (chromadb.Client): The ChromaDB client instance.
        collection_name (str): The name of the collection to create or reset.
        embedding_model (str): The embedding model to use for the collection.
        similarity_metric (str): Similarity metric used for calculating embedding distance

    Returns:
        chromadb.Collection: The created ChromaDB collection.
    """
    # Create a new collection with the specified embedding function
    db_collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(embedding_model, normalize_embeddings=True),
        metadata={"hnsw:space": similarity_metric},
    )
    return db_collection


def add_documents_to_chroma(collection: chromadb.Collection, id_document_pairs: Dict[str, Union[List[str], List[Document]]], document_prepend: str):
    """Add documents to a specified ChromaDB collection with optional metadata.

    Args:
        collection (chromadb.Collection): The ChromaDB collection to add documents to.
        id_document_pairs: Dict[str, Union[List[str], List[Document]]]: A Dict of IDs as keys and a list of Documents or strings as values
        document_prepend (str, optional): String to prepend to documents prior embedding)
    """

    # If values are Documents
    if isinstance(list(id_document_pairs.values())[0], Document):
        context_documents = list(id_document_pairs.values())
        context_texts = [f"{document_prepend} {doc.page_content}" for doc in context_documents]
        context_ids = list(id_document_pairs.keys())
        context_metadatas = [{"type": "context", **doc.metadata} for doc in context_documents]
    # If values are Strings
    else:
        context_texts = [f"{document_prepend} {doc}" for doc in id_document_pairs.values()]
        context_ids = list(id_document_pairs.keys())
        context_metadatas = [{"type": "context"} for _ in context_texts]

    collection.add(documents=context_texts, ids=context_ids, metadatas=context_metadatas)


def filter_context_candidates(
    chroma_db_collection,
    question_context_object: QuestionContextManager,
    top_k: int = 5,
    question_prepend: str = "query:",
    dist_threshold: float = 0,
    include_origin_context: bool = False,
) -> Dict[str, List[str]]:
    """
    Filters context candidates for each question based on similarity scores and optionally includes the original context.

    Parameters:
    - chroma_db_collection: The database collection to query for context candidates.
    - question_context_object: An object containing questions, contexts and queston-context ID pairs
    - top_k: The number of top results to consider from the query.
    - dist_threshold: The threshold for including additional contexts based on their distance from the ground truth context.
    - include_origin_context: A boolean to indicate whether the original context should be included in the results.

    Returns:
    - A dictionary mapping each question ID to a list of filtered context candidate IDs.
    """

    query_filtered = {}

    question_texts = [f"{question_prepend} {doc.page_content}" for doc in question_context_object.questions.values()]

    batch_query_result = chroma_db_collection.query(query_texts=question_texts, where={"type": "context"}, n_results=top_k)

    for idx, (q_id, q_document) in enumerate(question_context_object.questions.items()):
        query_id_list = batch_query_result["ids"][idx]
        query_distances_list = batch_query_result.get("distances", [])[idx]

        ground_truth_id = question_context_object.question_context_id_pairs[q_id][0]
        context_ids = []

        if ground_truth_id in query_id_list:
            gt_index = query_id_list.index(ground_truth_id)
            gt_distance = query_distances_list[gt_index]

            # Include higher-ranked items than the ground truth
            context_ids.extend(query_id_list[:gt_index])

            # Optionally include the ground truth
            if include_origin_context:
                context_ids.append(ground_truth_id)

            # Include lower-ranked items within the distance threshold
            for id_, distance in zip(query_id_list[gt_index + 1 :], query_distances_list[gt_index + 1 :]):
                if abs(distance - gt_distance) <= dist_threshold:
                    context_ids.append(id_)
        else:
            # If ground truth is not in the list, return the full list of querries (top_k)
            context_ids.extend(query_id_list)

        query_filtered[q_id] = context_ids

    return query_filtered


def c_eval_system_prompt():
    sys_prompt = """Din opgave er at evaluere hvorvidt et givent tekstuddrag indeholder svaret til et spørgsmål. Du skal alene vurdere om uddraget indeholder svaret, og ikke om svaret er korrekt.

    - Tildel scoren 1, hvis tekstuddraget indeholder svaret til spørgsmålet.

    - Tildel scoren 0, hvis tekstuddraget ikke kan bruges til at besvare spørgsmålet.
    """
    return sys_prompt


def c_eval_user_prompt(question: str, context: str) -> str:
    """Prepare the prompt for the API call."""

    qa_egnet_tmlp = """Din Opgave:
    
    Vurder om følgende spørgsmål kan besvares ud fra den givne kontekst i tekstuddraget:
    
    spørgsmål:
    {insert_question}
    
    tekstuddrag:
    {insert_context}
    
    Returner din vurdering i følgende JSON-format:

    {{
    "context_score": [indsæt enten 0 eller 1 her]
    }}
    """
    return qa_egnet_tmlp.format(insert_question=question, insert_context=context)


def context_question_llm_assesment(context_candidates, question_context_object: QuestionContextManager) -> Dict[str, List[str]]:
    """
    Iterates over the context candidate texts and uses a LLM call to assess whether the context matches the corresponding question

    Returns:
    A dictionary mapping each question ID to a list of context IDs, that according to the LLM can be used to answer the question
    """
    question_context_matches = {}
    system_prompt = c_eval_system_prompt()
    oai_client = OpenAI()

    for q_id, c_id_list in tqdm(context_candidates.items()):
        question_text = question_context_object.questions[q_id].page_content
        for c_id in c_id_list:
            context_text = question_context_object.contexts[c_id].page_content
            user_prompt = c_eval_user_prompt(question=question_text, context=context_text)
            response = json_api_call(oai_client, system_prompt, user_prompt)
            if response:
                if response["context_score"] == 1:
                    if q_id not in question_context_matches:
                        question_context_matches[q_id] = [c_id]
                    else:
                        question_context_matches[q_id].append(c_id)
                else:
                    continue
            else:
                logging.error(f"Failed to evaluate below text due to an earlier error. \n")
    return question_context_matches
