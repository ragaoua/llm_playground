from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector
import sys
from connect import get_pg_connection


def get_relevant_tickets(query):

    embedding_model = SentenceTransformer(
        "paraphrase-MiniLM-L3-v2", device="cuda"
    )
    query_embedding = embedding_model.encode(query)

    with get_pg_connection() as connection:
        register_vector(connection)
        with connection.cursor() as cursor:
            cursor.execute("""
               SELECT
                   t.tn,
                   c.conversation
               FROM ticket_conversation_embeddings e
               JOIN ticket_conversations c ON e.ticket_id = c.id
               JOIN ticket t ON t.id = e.ticket_id
               ORDER BY e.embedding <-> %s
               LIMIT 5;
           """, (query_embedding,))
            return cursor.fetchall()


if __name__ == '__main__':
    query = sys.argv[1]

    debug = False
    try:
        debug = sys.argv[2] == "DEBUG"
    except IndexError:
        pass

    relevant_tickets = get_relevant_tickets(query)

    for ticket in relevant_tickets:
        if debug:
            print("-------------------------------------------------")
            print("-------------------------------------------------")
            print("-------------------------------------------------")
            print("-------------------------------------------------")
            print("-------------------------------------------------")
            print("-------------------------------------------------")

        print(ticket[0])

        if debug:
            print(ticket[1])