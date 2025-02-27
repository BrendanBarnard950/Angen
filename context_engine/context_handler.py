from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from collections import Counter
import re
import uuid

class ContextHandler(object):
    # ============================================================================================================ #
    def __init__(self, db_path, collection_name = ""):
        if not (db_path == "" or collection_name == ""):
            self.chroma_client = PersistentClient(db_path)
            self.transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        else:
            raise Exception("Please provide a path to where we should save your collection")
    
    # ============================================================================================================ #    
    def process_prompt(self, prompt):
        """
        Takes the user's prompt, embedds it, searches our DB, and comes back with data.
        """
        
        embedded_prompt = self.transformer_model.encode(prompt)
        
        # Get all the queries that fit the embedded prompt.
        query_results = self.collection.query(
            query_embeddings=[embedded_prompt],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )
        
        # This is a little cursed. Unpacking the query results took SO long to figure out.
        # ToDo: Make this a little less painful to look at
        final_prompt_list = []
        final_prompt = prompt + "\n\nPlease answer according to the information bellow. The sections are ordered by relevance."
        for tags, text, distance in zip(query_results["metadatas"][0], query_results["documents"][0], query_results["distances"][0]):
            tag_multiplier = 0
            prompt_words = re.findall(r'\b\w+\b', prompt.lower())
            
            result_tags_counter = Counter(tags['tags'])
            prompt_words_counter = Counter(prompt_words)
            
            tag_multiplier = sum(min(result_tags_counter[tag], prompt_words_counter[tag]) for tag in result_tags_counter if tag in prompt_words_counter)
              
                
            weight = distance * tag_multiplier
            final_prompt_list.append({'text': text, 'weight': weight})
            
        final_prompt_list = sorted(final_prompt_list, key=lambda d: d['weight'])
        
        for text in final_prompt_list:
            final_prompt += ("\n\n%s" % text['text'])
        
        return final_prompt 
    
    # ============================================================================================================ #      
    def process_context(self, context, tags, category):
        """
        Processes a large string into manageable chunks, then embedds them and pops them onto the
        ChromaDB database
        """
        chunked_context = self.chunk(context)
        chunk_id_list = []
        embeddings_list = []
        tags_list = []
        chunk_strings = []
        
        for chunk in chunked_context:
            # Use UUID for uniqueness, otherwise we might accidentally overrite old chunks
            # I'm slightly regretting this. Storage looks strange,but it's so small that I'm not gonna worry about it
            # ToDo: See if/how auto-incrementing works with ChromaDB? UUID might scale poorly
            chunk_id = str(uuid.uuid4())
            embeddings = self.transformer_model.encode(chunk)
            chunk_id_list.append(chunk_id)
            embeddings_list.append(embeddings)
            tags_list.append({"category": category, "tags":tags})         
            chunk_strings.append(chunk) 
            
        self.collection.add(
            ids = chunk_id_list,
            embeddings=embeddings_list,
            metadatas=tags_list,
            documents=chunk_strings
        )
        
    # ============================================================================================================ #
    def chunk(self, context):
        """
        Chunks text. This is the part where we'll probably be able to get most of our
        performance increases. For now having our stuff in Markdown format would work best.
        Honestly the performance of PDF and DOCX is gonig to be bad because the markdown
        conversion is still ass for the time being.
        
        Chunking is being fine-tuned. For now, chunks will be the lowest wordcount aboce 250 words
        that does NOT split a sentence in half.
        
        ToDo: Checks for dialogue tags, so we dont cut before a character's dialogue is one.
        ex: "Are you busy?" John asked  -  That would cut at the ?, costing us context
        """
        
        context_sections = re.split(r"\n\s*(#+|\d+\.)\s*\w+", context)
        
        cleaned_context = [section.strip() for section in context_sections if section.strip()]
        
        
        # The chunks turned out way too big, so I'm doing another round of breaking. I am going
        # to break it up into individual paragraphs, trying to include the last line of the
        # previous chunk to try to keep up contextual continuity
        final_context = []
        previous_last_sentence = ""
        
        # There has to be a better way to do this. Nested fors cause severe pain, but for now
        # I can't think of a better way.
        # ToDo: Make this not bad.
        for chunk in cleaned_context:
            paragraphs = re.split(r"\n\s*", chunk)
            cleaned_paragraphs = [p.strip() for p in paragraphs if p.strip()]
            sentences = re.split(r"(?<=[.!?])\s+", " ".join(cleaned_paragraphs))
            
            current_chunk = previous_last_sentence
            
            for sentence in sentences:
                current_chunk += " " + sentence
                word_count = len(current_chunk.strip().split())
                
                if word_count >= 250:
                    final_context.append(current_chunk.strip())
                    current_chunk = sentence
            
        # Adding any straggling text that didn't make the cut in the other chunks
        if current_chunk.strip():
            final_context.append(current_chunk.strip())
    
        previous_last_sentence = sentences[-1] if sentences else ""
        
        return final_context
        